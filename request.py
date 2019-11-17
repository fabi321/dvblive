import requests
import xml_requests
from xml.etree import ElementTree
import time
import datetime
from typing import List, Dict, Tuple
from Classes.LocationResponse import LocationResponse
from Classes.Station import Station
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



def request_location_informaiton(station: Station):
    request: str = xml_requests.location_information_request_stop.replace('$STATION', str(station))
    r = requests.post(url, request, headers=headers)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: LocationResponse = LocationResponse(tree)
    station.set_location(request_element.get_cords())


def stop_request(station: Station, request_time: int, number: int):
    request: str = xml_requests.stop_request.replace('$STATION', str(station))
    request_time = unix_time_to_iso(request_time)
    request = request.replace('$TIME', request_time)
    request = request.replace('$NUMBER_OF_RESULTS', str(number))
    r = requests.post(url, request, headers=headers)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: StopResponse = StopResponse(tree)
    return request_element


def trip_request(start_station: Station, stop_station: Station, request_time: int, polygons: bool = False):
    request_time = unix_time_to_iso(request_time)
    request: str = xml_requests.trip_request.replace('$START_ID', str(start_station))
    request = request.replace('$STOP_ID', str(stop_station))
    request = request.replace('$TIME', request_time)
    if polygons:
        request.replace('$POLYGONS', '')
    else:
        request.replace('$POLYGONS', '<IncludeLegProjection>true</IncludeLegProjection>')
    r = requests.post(url, request, headers=headers)
    tree: List[ElementTree.ElementTree] = ElementTree.fromstring(r.content)
    request_element: TripResponse = TripResponse(tree)
    return request_element


class ParallelLocation(threading.Thread):
    def __init__(self, q: queue.Queue):
        threading.Thread.__init__(self)
        self._q: queue.Queue = q

    def run(self):
        while not self._q.empty():
            queue_lock.acquire()
            station: Station = self._q.get()
            queue_lock.release()
            request_location_informaiton(station)


def parallel_location(stations: List[Station], threads: int = 20):
    work_queue: queue.Queue = queue.Queue()
    thread_list: List[ParallelLocation] = []
    for i in stations:
        work_queue.put(i)
    for i in range(threads):
        thread = ParallelLocation(work_queue)
        thread.start()
        thread_list.append(thread)
    for i in thread_list:
        i.join()


stop_response_list: List[StopResponse] = []


class ParallelStop(threading.Thread):
    def __init__(self, q: queue.Queue):
        threading.Thread.__init__(self)
        self._q: queue.Queue = q

    def run(self):
        while not self._q.empty():
            queue_lock.acquire()
            data: Dict = self._q.get()
            queue_lock.release()
            stop_response: StopResponse = stop_request(data['station'], data['request_time'], data['number'])
            queue_lock.acquire()
            stop_response_list.append(stop_response)
            queue_lock.release()


def parallel_stop(data: List[Dict], threads: int = 20):
    work_queue: queue.Queue = queue.Queue()
    stop_response_list.clear()
    thread_list: List[ParallelStop] = []
    for i in data:
        work_queue.put(i)
    for i in range(threads):
        thread = ParallelStop(work_queue)
        thread.start()
        thread_list.append(thread)
    for i in thread_list:
        i.join()
    return stop_response_list


trip_response_list: [List[TripResponse], List[Tuple[TripResponse, str]]] = []


class ParallelTrip(threading.Thread):
    def __init__(self, q: queue.Queue):
        threading.Thread.__init__(self)
        self._q: queue.Queue = q

    def run(self):
        while not self._q.empty():
            queue_lock.acquire()
            data: Dict = self._q.get()
            queue_lock.release()
            if type(data) == dict:
                trip_response: TripResponse = trip_request(data['start_station'], data['stop_station'], data['request_time'], data['polygon'])
            else:
                trip_response: Tuple[TripResponse, str] = (trip_request(data[0]['start_station'], data[0]['stop_station'],
                                                           data[0]['request_time'], data[0]['polygon']), data[1])
            queue_lock.acquire()
            trip_response_list.append(trip_response)
            queue_lock.release()


def parallel_trip(data: [List[Dict], List[Tuple[Dict, str]]], threads: int = 20):
    work_queue: queue.Queue = queue.Queue()
    trip_response_list.clear()
    thread_list: List[ParallelTrip] = []
    for i in data:
        work_queue.put(i)
    for i in range(threads):
        thread = ParallelTrip(work_queue)
        thread.start()
        thread_list.append(thread)
    for i in thread_list:
        i.join()
    return trip_response_list
