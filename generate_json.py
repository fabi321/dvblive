import json
from typing import Dict, List, Tuple, Any
from fetch_init import output_format
from Classes.Line import Line
from Classes.Stop import Stop
from Classes.Section import Section
from Classes import Location
import logging

logger = logging.getLogger('generate_json')


def generate_json(tuple: output_format) -> Tuple[str, str]:
    abschnitte: List[Dict[str, Any]] = []
    stops: List[Stop] = tuple[1]
    sections: Dict[str, Section] = tuple[2]
    logger.info('Generating sections json.')
    for i, j in sections.items():
        entry: Dict[str, object] = {}
        entry.update({'start': str(j.get_start_stop())})
        entry.update({'end': str(j.get_end_stop())})
        entry.update({'maxVerspaetung': 0})
        start_location: Location = j.get_start_stop().get_location()
        entry.update({'startPosition': start_location})
        end_location: Location = j.get_end_stop().get_location()
        entry.update({'startPosition': end_location})
        polygon: List[Location] = j.get_polygon()
        entry.update({'polygon': polygon})
        lines: List[str] = []
        for h in j.get_lines():
            lines.append(str(h.get_line_number()))
        entry.update({'linien': lines})
        abschnitte.append(entry)
    abschnitte_json: str = json.dumps(abschnitte)
    logger.info('Generated sections json.')
    haltestellen: List[Dict[str, str]] = []
    logger.info('Generating haltestellen json.')
    for i in stops:
        entry: Dict[str, str] = {}
        entry.update({'triasCode': str(i)})
        entry.update(i.get_location())
        haltestellen.append(entry)
    haltestellen_json = json.dumps(haltestellen)
    logger.info('Generated haltestellen json')
    return abschnitte_json, haltestellen_json
