from typing import List, Dict, Tuple
from Classes.Line import Line
from Classes.TripResponse import TripResponse
from Classes.Station import Station
from Classes.Section import Section
from Classes.StopResponse import StopResponse
import time
from request import parallel_location, parallel_stop, parallel_trip
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger: logging.Logger = logging.getLogger('main')

zeit1 = time.time()
request_time = time.time()
base_stations: List[str] = ['de:14612:13', 'de:14612:5', 'de:14612:7']
base_dicts: List[Dict] = []
for i in base_stations:
    base_dicts.append({'station': i, 'request_time': time.time(), 'number': 15})
logger.info('Getting lines from base stations.')
trams: List[StopResponse] = parallel_stop(base_dicts)
unique_lines: List[Line] = []
for i in trams:
    for i in i.get_lines():
        if not any([str(i) == str(j) for j in unique_lines]):
            unique_lines.append(i)
logger.info('Got ' + str(len(unique_lines)) + ' lines.')
trips: List[Dict] = []
for i in unique_lines:
    trips.append({'start_station': i.get_stations()[0], 'stop_station': i.get_stations()[1], 'request_time': time.time(), 'polygon': False})
logger.info('Getting lines from start and end stops.')
lines: List[TripResponse] = parallel_trip(trips)
unique_stations: List[Station] = []
for i in lines:
    for i in i.get_stations():
        if unique_stations.count(i) == 0:
            unique_stations.append(i)
        else:
            index = unique_stations.index(i)
            unique_stations[index] += i
logger.info('Got ' + str(len(unique_stations)) + ' Stations from lines')
logger.info('Getting locations for stations')
parallel_location(unique_stations)
logger.info('Got locations for ' + str(len(unique_stations)) + ' stations')
logger.info('Uniquifying lines in stations')
for i in unique_stations:
    i.unique_lines()
sections: List[Section] = []
logger.info('Getting sections from lines')
for i in lines:
    sections += i.get_sections()
unique_sections: Dict[str, Section] = {}
logger.info('Uniquifying sections')
for i in sections:
    try:
        unique_sections[str(i)] += i
    except KeyError:
        unique_sections.update({str(i): i})
logger.info('Uniquifyed ' + str(len(unique_sections)) + ' sections.')
print(time.time()-zeit1)
trips: List[Tuple[Dict, str]] = []
for i, j in unique_sections.items():
    trips.append(({'start_station': j.get_start_station(), 'stop_station': j.get_end_station(), 'request_time': time.time(), 'polygon': True}, i))
logger.info('Getting polygons for section')
polygons: List[Tuple[TripResponse, str]] = parallel_trip(trips, 40)
logger.info('Got polygons for ' + str(len(unique_sections)) + ' sections.')
logger.info('Apolying polygons to sections')
for i in polygons:
    unique_sections[i[1]].set_polygon(i[0].get_cords())
print(time.time()-zeit1)

