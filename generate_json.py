import json
import logging
import time
from typing import Dict, List, Tuple, Any

import ZODB.config
from ZODB.Connection import Connection

from Classes.BaseTypes.Time import Time
from Classes.DBManager.DBLine import DBLine
from Classes.DBManager.DBSection import DBSection
from Classes.DBManager.DBStop import DBStop
from Classes.DBManager.DBTime import DBTime
from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import Location

logger = logging.getLogger('generate_json')

db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)


def generate_json() -> Tuple[str, str]:
    connection: Connection = db.open()
    abschnitte: List[Dict[str, Any]] = []
    db_lines: DBLine = connection.root().lines
    db_stops: DBStop = connection.root().stops
    db_sections: DBSection = connection.root().sections
    db_times: DBTime = connection.root().times
    logger.info('Generating sections json.')
    for section_id, section in db_sections:
        times_within_half_hour: List[Time] = []
        for i, j in db_times.get_times_for_section(section_id):
            if i.get_planned() > time.time() - 30 * 60:
                times_within_half_hour.append(i)
        sum: int = 0
        for i in times_within_half_hour:
            sum += i.get_difference()
        if len(times_within_half_hour) >= 1:
            average: int = int(sum / len(times_within_half_hour))
        else:
            average: int = 0
        entry: Dict[str, object] = {}
        entry.update({'start': str(section.get_start_stop())})
        entry.update({'end': str(section.get_end_stop())})
        entry.update({'maxVerspaetung': average})
        start_location: Location = section.get_start_stop().get_location()
        entry.update({'startPosition': start_location})
        end_location: Location = section.get_end_stop().get_location()
        entry.update({'startPosition': end_location})
        polygon: List[Location] = section.get_polygon()
        entry.update({'polygon': polygon})
        lines: List[str] = []
        for j in section.get_lines():
            lines.append(str(j.get_line_number()))
        entry.update({'linien': lines})
        abschnitte.append(entry)
    abschnitte_json: str = json.dumps(abschnitte)
    logger.info('Generated sections json.')
    haltestellen: List[Dict[str, str]] = []
    logger.info('Generating haltestellen json.')
    for _, stop in db_stops:
        entry: Dict[str, str] = {}
        entry.update({'triasCode': str(stop), 'stopName': stop.get_name()})
        entry.update(stop.get_location())
        haltestellen.append(entry)
    haltestellen_json = json.dumps(haltestellen)
    logger.info('Generated haltestellen json')
    connection.close()
    return abschnitte_json, haltestellen_json
