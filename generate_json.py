import json
from typing import Dict, List, Tuple, Any
from fetch_init import output_format
from Classes.Line import Line
from Classes.MergeableList import MergeableList
from Classes.Stop import Stop
from Classes.Section import Section
from Classes.Time import Time
from Classes import Location
import logging
import time

logger = logging.getLogger('generate_json')


def generate_json(tuple: output_format) -> Tuple[str, str]:
    abschnitte: List[Dict[str, Any]] = []
    lines: MergeableList = tuple[0]
    stops: MergeableList = tuple[1]
    sections: MergeableList = tuple[2]
    logger.info('Generating sections json.')
    for i in sections:
        times: List[Time] = []
        for j in lines:
            if isinstance(j, Line):
                for k in j.get_stops():
                    if str(k) in str(i).split('=|='):
                        times += j.get_journeys_for_section_id(str(i))
        times_within_half_hour: List[Time] = []
        for j in times:
            if j.get_planned() > time.time():
                times_within_half_hour.append(j)
        sum: int = 0
        for j in times_within_half_hour:
            sum += j.get_difference()
        if len(times_within_half_hour) >= 1:
            average: int = int(sum / len(times_within_half_hour))
        else:
            average: int = 0
        entry: Dict[str, object] = {}
        entry.update({'start': str(i.get_start_stop())})
        entry.update({'end': str(i.get_end_stop())})
        entry.update({'maxVerspaetung': average})
        start_location: Location = i.get_start_stop().get_location()
        entry.update({'startPosition': start_location})
        end_location: Location = i.get_end_stop().get_location()
        entry.update({'startPosition': end_location})
        polygon: List[Location] = i.get_polygon()
        entry.update({'polygon': polygon})
        lines: List[str] = []
        for j in i.get_lines():
           lines.append(str(j.get_line_number()))
        entry.update({'linien': lines})
        abschnitte.append(entry)
    abschnitte_json: str = json.dumps(abschnitte)
    logger.info('Generated sections json.')
    haltestellen: List[Dict[str, str]] = []
    logger.info('Generating haltestellen json.')
    for i in stops:
        entry: Dict[str, str] = {}
        entry.update({'triasCode': str(i), 'stopName': i.get_name()})
        entry.update(i.get_location())
        haltestellen.append(entry)
    haltestellen_json = json.dumps(haltestellen)
    logger.info('Generated haltestellen json')
    return abschnitte_json, haltestellen_json
