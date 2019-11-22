from typing import List, Dict, Tuple, Any
from Classes.Line import Line
from Classes.TripResponse import TripResponse
from Classes.Stop import Stop
from Classes.Section import Section
from Classes.StopResponse import StopResponse
import datetime
from request import parallel_location, parallel_stop, parallel_trip
import logging
import time

logger: logging.Logger = logging.getLogger('fetch_init')
output_format = Tuple[List[Line], List[Stop], Dict[str, Section]]


def fetch_init(debug: bool = False) -> output_format:
    start_time: float = time.time()
    request_parallelisation: int = 20
    if debug:
        request_parallelisation: int = 1
    request_time: datetime.datetime = datetime.datetime.now()
    request_time: datetime.datetime = request_time.replace(hour=12, minute=30, second=0)
    request_time: int = int(request_time.timestamp())
    base_stops: List[str] = ['de:14612:13', 'de:14612:5', 'de:14612:7']
    base_dicts: List[List[Any]] = []
    for i in base_stops:
        base_dicts.append([i, request_time, 15])
    logger.info('Getting lines from base stops.')
    lines: List[StopResponse] = parallel_stop(base_dicts, debug=debug, threads=request_parallelisation, calculate_lines=True)
    unique_lines: List[Line] = []
    for i in lines:
        for i in i.get_lines():
            if not any([str(i) == str(j) for j in unique_lines]):
                unique_lines.append(i)
    logger.info('Got ' + str(len(unique_lines)) + ' lines.')
    trips: List[List[Any]] = []
    kwargs: List[Dict[str, Any]] = []
    for i in unique_lines:
        trips.append(
            [i.get_stops()[0], i.get_stops()[1], request_time])
        kwargs.append({'line_trias_id': str(i), 'debug': debug, 'calculate_stops': True, 'calculate_sections': True})
    logger.info('Getting lines from start and end stops.')
    lines: List[TripResponse] = parallel_trip(trips, debug=debug, threads=request_parallelisation, kwargs=kwargs)
    unique_stops: List[Stop] = []
    for i in lines:
        for i in i.get_stops():
            if unique_stops.count(i.get_base_stop()) == 0:
                unique_stops.append(i.get_base_stop())
            else:
                index = unique_stops.index(i.get_base_stop())
                unique_stops[index] += i
    logger.info('Got ' + str(len(unique_stops)) + ' Stops from lines')
    logger.info('Getting locations for stops')
    unique_stops = parallel_location(unique_stops)
    logger.info('Got locations for ' + str(len(unique_stops)) + ' stops')
    logger.info('Uniquifying lines in stops')
    for i in unique_stops:
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
    trips: List[List[Any]] = []
    kwargs: List[Dict[str, Any]] = []
    for i, j in unique_sections.items():
        trips.append([j.get_start_stop(), j.get_end_stop(),
                       request_time])
        kwargs.append({'debug': debug, 'id': i, 'polygons': True, 'line_trias_id': str(j.get_lines()[0])})
    logger.info('Getting polygons for section')
    polygons: List[Tuple[str, TripResponse]] = parallel_trip(trips, threads=request_parallelisation * 2, kwargs=kwargs)
    logger.info('Got polygons for ' + str(len(unique_sections)) + ' sections.')
    logger.info('Apylying polygons to sections')
    for i in polygons:
        unique_sections[i[0]].set_polygon(i[1].get_cords())
    logger.info('Applied polygons to sections')
    logger.info('Fetched init_data in ' + str(int(time.time() - start_time)) + ' seconds.')
    return unique_lines, unique_stops, unique_sections

