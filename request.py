import requests
import xml_requests
from xml.etree import ElementTree
import time
import datetime
from typing import List, Dict, Tuple, Any
from Classes.LocationResponse import LocationResponse
from Classes.StopWithoutLine import StopWithoutLine
from Classes.StopResponse import StopResponse
from Classes.TripResponse import TripResponse
import threading
from multiprocessing import Pool

queue_lock: threading.Lock = threading.Lock()

url = 'http://efa.vvo-online.de:8080/std3/trias'
headers = {'Content-Type': 'text/xml'}


def unix_time_to_iso(input_time: int) -> str:
    input_time: datetime.datetime = datetime.datetime.utcfromtimestamp(input_time)
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return input_time.replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


def worker(args_kwargs: Tuple[Any, List[Any], Dict[str, Any]]):
    return args_kwargs[0](*args_kwargs[1], **args_kwargs[2])


def parallelise(function: Any, args: List[List[Any]], kwargs: List[Dict[str, Any]], threads: int = 20, **call_kwargs):
    worker_list: List[Tuple[Any, List[Any], Dict[str, Any]]] = []
    if len(kwargs) == 1:
        for i in args:
            worker_list.append((function, i, kwargs[0]))
    else:
        for i in range(len(args)):
            worker_list.append((function, args[i], kwargs[i]))
    with Pool(threads) as p:
        return p.map(worker, worker_list)


def request_location_informaiton(stop: StopWithoutLine, **kwargs):
    if stop.has_location():
        return
    request: str = xml_requests.location_information_request_stop.replace('$STATION', str(stop))
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: LocationResponse = LocationResponse(tree)
    stop.set_location(request_element.get_cords())
    return stop


def stop_request(stop: StopWithoutLine, request_time: int, number: int, **kwargs):
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
    request_element: StopResponse = StopResponse(tree, **kwargs)
    # pre-calculate elements to save time at not multiprocessed parts
    if kwargs.get('calculate_lines'):
        request_element.get_lines()
    if kwargs.get('calculate_journeys'):
        request_element.get_journeys()
    return request_element


def trip_request(start_stop: StopWithoutLine, end_stop: StopWithoutLine, request_time: int, **kwargs):
    request_time = unix_time_to_iso(request_time)
    request: str = xml_requests.trip_request.replace('$START_ID', str(start_stop))
    request = request.replace('$STOP_ID', str(end_stop))
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


def stop_name_request(name: str):
    request: str = xml_requests.stop_name_request.replace('$NAME', name)
    while True:
        r = requests.post(url, request, headers=headers)
        if r.ok:
            break
        else:
            time.sleep(1)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    return tree


def parallel_location(stops: List[StopWithoutLine], threads: int = 20, **kwargs):
    args: List[List[StopWithoutLine]] = []
    for i in stops:
        args.append([i])
    return parallelise(request_location_informaiton, args, [kwargs], threads=threads)


def parallel_stop(data: List[List[Any]], threads: int = 20, **kwargs):
    stop_response_list = parallelise(stop_request, data, [kwargs], threads=threads)
    return stop_response_list


def parallel_trip(data: List[List[Any]], threads: int = 20, kwargs: List[Dict[str, Any]] = None, **call_kwargs):
    if kwargs:
        trip_response_list = parallelise(trip_request, data, kwargs, threads=threads)
    else:
        trip_response_list = parallelise(trip_request, data, [call_kwargs], threads=threads)
    return trip_response_list
