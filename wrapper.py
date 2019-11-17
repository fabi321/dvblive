from typing import List, Dict, Tuple
from Classes.Line import Line
from Classes.TripResponse import TripResponse
from Classes.Station import Station
from Classes.Section import Section
import time
from request import parallel_location, parallel_stop, parallel_trip

zeit1 = time.time()
request_time = time.time()
base_stations: List[str] = ['de:14612:13', 'de:14612:5', 'de:14612:7']
base_dicts: List[Dict] = []
for i in base_stations:
    base_dicts.append({'station': i, 'request_time': time.time(), 'number': 15})
trams = parallel_stop(base_dicts)
unique_lines: List[Line] = []
for i in trams:
    for i in i.get_lines():
        if not any([str(i) == str(j) for j in unique_lines]):
            unique_lines.append(i)
trips: List[Dict] = []
for i in unique_lines:
    trips.append({'start_station': i.get_stations()[0], 'stop_station': i.get_stations()[1], 'request_time': time.time(), 'polygon': False})
lines: List[TripResponse] = parallel_trip(trips)
unique_stations: List[Station] = []
for i in lines:
    for i in i.get_stations():
        if unique_stations.count(i) == 0:
            unique_stations.append(i)
        else:
            index = unique_stations.index(i)
            unique_stations[index] += i
parallel_location(unique_stations)
for i in unique_stations:
    i.unique_lines()
sections: List[Section] = []
for i in lines:
    sections += i.get_sections()
unique_sections: Dict[str, Section] = {}
for i in sections:
    try:
        unique_sections[str(i)] += i
    except KeyError:
        unique_sections.update({str(i): i})
print(time.time()-zeit1)
trips: List[Tuple[Dict, str]] = []
for i, j in unique_sections.items():
    trips.append(({'start_station': j.get_start_station(), 'stop_station': j.get_end_station(), 'request_time': time.time(), 'polygon': True}, i))
polygons: List[Tuple[TripResponse, str]] = parallel_trip(trips)
for i in polygons:
    unique_sections[i[1]].set_polygon(i[0].get_cords())
print(time.time()-zeit1)

