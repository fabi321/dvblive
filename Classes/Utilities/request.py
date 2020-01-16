import datetime
import queue
import threading
import time
from multiprocessing import Pool
from typing import List, Dict, Tuple, Any, Callable, Sequence, Optional, Union
from xml.etree import ElementTree

import ZODB.config
import requests
from ZODB.Connection import Connection
from transaction import commit

from Classes.BaseTypes.StopWithoutLine import StopWithoutLine
from Classes.DBManager.DBStopWithoutLine import DBStopWithoutLine
from Classes.LowRequests.LocationResponse import LocationResponse
from Classes.LowRequests.StopResponse import StopResponse
from Classes.LowRequests.TripResponse import TripResponse
from Classes.Utilities import xml_requests
from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import UnixTime, ISOTimeStr, StopWithoutLineStr, StopStr

queue_lock: threading.Lock = threading.Lock()

url = 'http://efa.vvo-online.de:8080/std3/trias'
headers = {'Content-Type': 'text/xml'}
use_multiprocessing = True

db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)


class Parallelize(threading.Thread):
    def __init__(self, q: queue.Queue):
        threading.Thread.__init__(self)
        self._q: queue.Queue = q

    def run(self):
        while not self._q.empty():
            queue_lock.acquire()
            data: Tuple[Callable, Sequence[Any], Dict[str, Any], List[Any]] = self._q.get()
            queue_lock.release()
            data[3].append(data[0](*data[1], **data[2]))


def parallelize(function: Callable, args: Sequence[Sequence[Any]], kwargs: Sequence[Dict[str, Any]], threads: int = 20,
                **call_kwargs):
    worker_list: List[Tuple[Callable, Sequence[Any], Dict[str, Any]]] = []
    if len(kwargs) == 1:
        for i in args:
            worker_list.append((function, i, kwargs[0]))
    else:
        for i in range(len(args)):
            worker_list.append((function, args[i], kwargs[i]))
    if use_multiprocessing:
        with Pool(threads) as p:
            return p.map(worker, worker_list)
    work_queue: queue.Queue = queue.Queue()
    thread_list: List[Parallelize] = []
    output_list: List[Any] = []
    for i in worker_list:
        work_queue.put((i[0], i[1], i[2], output_list))
    for i in range(threads):
        thread = Parallelize(work_queue)
        thread.start()
        thread_list.append(thread)
    for i in thread_list:
        i.join()
    return output_list


def unix_time_to_iso(input_time: UnixTime) -> ISOTimeStr:
    input_time: datetime.datetime = datetime.datetime.fromtimestamp(input_time)
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return ISOTimeStr(input_time.replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat())


def worker(args_kwargs: Tuple[Any, List[Any], Dict[str, Any]]):
    return args_kwargs[0](*args_kwargs[1], **args_kwargs[2])


def request_location_information(stop: StopWithoutLineStr, **kwargs) -> StopWithoutLineStr:
    connection: Connection = db.open()
    stops: DBStopWithoutLine = connection.root().stops
    current_stop: StopWithoutLine = stops[stop]
    if current_stop.has_location():
        return stop
    request: str = xml_requests.location_information_request_stop.replace('$STATION', stop)
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: LocationResponse = LocationResponse(tree)
    current_stop.set_location(request_element.get_cords())
    commit()
    return stop


def stop_request(stop: StopWithoutLineStr, request_time: UnixTime, number: int, **kwargs) -> \
        [List[ElementTree.ElementTree], StopResponse]:
    request: str = xml_requests.stop_request.replace('$STATION', str(stop))
    request_time: str = unix_time_to_iso(request_time)
    request = request.replace('$TIME', request_time)
    request = request.replace('$NUMBER_OF_RESULTS', str(number))
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    if kwargs.get('return_tree'):
        return tree
    calculate_lines: bool = 'calculate_lines' in kwargs.keys()
    request_element: StopResponse = StopResponse(tree, **kwargs)
    # pre-calculate elements to save time at not multiprocessed parts
    if calculate_lines:
        request_element.get_lines()
    return request_element


def trip_request(start_stop: StopWithoutLineStr, end_stop: StopWithoutLineStr, request_time: UnixTime, **kwargs) -> \
        [List[ElementTree.ElementTree], TripResponse, Tuple[Optional[Any], TripResponse]]:
    request_time: ISOTimeStr = unix_time_to_iso(request_time)
    request: str = xml_requests.trip_request.replace('$START_ID', start_stop)
    request = request.replace('$STOP_ID', end_stop)
    request = request.replace('$TIME', request_time)
    if kwargs.get('polygons'):
        request = request.replace('$POLYGONS', '<IncludeLegProjection>true</IncludeLegProjection>')
    else:
        request = request.replace('$POLYGONS', '')
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        else:
            time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    if kwargs.get('return_tree'):
        return tree
    request_element: TripResponse = TripResponse(tree, **kwargs)
    # pre-calculate elements to save time at not multiprocessed parts
    if kwargs.get('polygons'):
        request_element.get_cords()
    if kwargs.get('calculate_lines'):
        request_element.get_line()
    if kwargs.get('calculate_stops'):
        request_element.get_stops()
    if kwargs.get('calculate_sections'):
        request_element.get_sections()
    if kwargs.get('id'):
        return kwargs.get('id'), request_element
    return request_element


def stop_name_request(name: str) -> List[ElementTree.ElementTree]:
    request: str = xml_requests.stop_name_request.replace('$NAME', name)
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        else:
            time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    return tree


def parallel_location(stops: Sequence[Union[StopWithoutLineStr, StopStr]], threads: int = 20, **kwargs) -> \
        List[Union[StopWithoutLineStr, StopStr]]:
    args: List[List[StopWithoutLineStr]] = []
    for i in stops:
        args.append([i])
    return parallelize(request_location_information, args, [kwargs], threads=threads)


def parallel_stop(data: Sequence[Tuple[StopWithoutLineStr, UnixTime, int]], threads: int = 20, **kwargs) -> \
        List[StopResponse]:
    stop_response_list = parallelize(stop_request, data, [kwargs], threads=threads)
    return stop_response_list


def parallel_trip(data: Sequence[Tuple[StopWithoutLineStr, StopWithoutLineStr, UnixTime]], threads: int = 20,
                  kwargs: List[Dict[str, Any]] = None, **call_kwargs) -> \
        List[TripResponse]:
    if kwargs:
        trip_response_list = parallelize(trip_request, data, kwargs, threads=threads)
    else:
        trip_response_list = parallelize(trip_request, data, [call_kwargs], threads=threads)
    return trip_response_list
