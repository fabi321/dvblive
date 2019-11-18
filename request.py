import requests
import xml_requests
from xml.etree import ElementTree
import time
import datetime
from typing import List, Dict, Tuple, Any
from Classes.LocationResponse import LocationResponse
from Classes.Stop import Stop
from Classes.StopResponse import StopResponse
from Classes.TripResponse import TripResponse
import threading
import queue

queue_lock: threading.Lock = threading.Lock()

url = 'http://efa.vvo-online.de:8080/std3/trias'
headers = {'Content-Type': 'text/xml'}


def unix_time_to_iso(input_time: int) -> str:
    input_time: datetime.datetime = datetime.datetime.utcfromtimestamp(input_time)
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return input_time.replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


class Parallelise(threading.Thread):
    def __init__(self, q: queue.Queue):
        threading.Thread.__init__(self)
        self._q: queue.Queue = q

    def run(self):
        while not self._q.empty():
            queue_lock.acquire()
            data: Tuple[Any, List[Any], Dict[str, Any], List[Any]] = self._q.get()
            queue_lock.release()
            data[3].append(data[0](*data[1], **data[2]))


def parallelise(function: Any, args: List[List[Any]], kwargs: List[Dict[str, Any]], threads: int = 20):
    work_queue: queue.Queue = queue.Queue()
    thread_list: List[Parallelise] = []
    output_list: List[Any] = []
    if len(kwargs) == 1:
        for i in args:
            work_queue.put((function, i, kwargs[0], output_list))
    else:
        for i in range(len(args)):
            work_queue.put((function, args[i], kwargs[i], output_list))
    for i in range(threads):
        thread = Parallelise(work_queue)
        thread.start()
        thread_list.append(thread)
    for i in thread_list:
        i.join()
    return output_list


def request_location_informaiton(stop: Stop, debug: bool = False):
    request: str = xml_requests.location_information_request_stop.replace('$STATION', str(stop))
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: LocationResponse = LocationResponse(tree)
    stop.set_location(request_element.get_cords())


def stop_request(stop: Stop, request_time: int, number: int, debug: bool = False):
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
    request_element: StopResponse = StopResponse(tree)
    return request_element


def trip_request(start_stop: Stop, end_stop: Stop, request_time: int, polygons: bool = False, debug: bool = False, id: str = None):
    request_time = unix_time_to_iso(request_time)
    request: str = xml_requests.trip_request.replace('$START_ID', str(start_stop))
    request = request.replace('$STOP_ID', str(end_stop))
    request = request.replace('$TIME', request_time)
    if polygons:
        request = request.replace('$POLYGONS', '<IncludeLegProjection>true</IncludeLegProjection>')
    else:
        request = request.replace('$POLYGONS', '')
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: TripResponse = TripResponse(tree)
    if debug:
        request_element.get_stops()
    if polygons:
        request_element.get_cords()
    if id:
        return id, request_element
    return request_element


def parallel_location(stops: List[Stop], debug: bool = False, threads: int = 20):
    args: List[List[Stop]] = []
    for i in stops:
        args.append([i])
    parallelise(request_location_informaiton, args, [{'debug': debug}], threads=threads)


def parallel_stop(data: List[List[Any]], debug: bool = False, threads: int = 20):
    stop_response_list = parallelise(stop_request, data, [{'debug': debug}], threads=threads)
    return stop_response_list


def parallel_trip(data: List[List[Any]], debug: bool = False, threads: int = 20, kwargs: List[Dict[str, Any]] = None):
    if kwargs:
        trip_response_list = parallelise(trip_request, data, kwargs, threads=threads)
    else:
        trip_response_list = parallelise(trip_request, data, [{'debug': debug}], threads=threads)
    return trip_response_list
