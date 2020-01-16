import logging
import time
from multiprocessing import Pool
from typing import List, Any, Tuple, Dict

import ZODB.config
from ZODB.Connection import Connection

from Classes.DBManager.DBJourney import DBJourney
from Classes.DBManager.DBLine import DBLine
from Classes.DBManager.DBSection import DBSection
from Classes.DBManager.DBStop import DBStop
from Classes.HighRequests.IDStopResponse import IDStopResponse
from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import UnixTime, StopWithoutLineStr, JourneyStr

logger: logging.Logger = logging.getLogger('fetch_live')

db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)


def worker(args_kwargs: Tuple[StopWithoutLineStr, UnixTime, Dict[str, Any]]):
    return IDStopResponse(args_kwargs[0], args_kwargs[1], **args_kwargs[2])


def fetch_live():
    connection: Connection = db.open()
    start_time: UnixTime = UnixTime(int(time.time()))
    logger.info('Fetching live data')
    db_stops: DBStop = connection.root().stops
    args: List[Tuple[Any, int, Dict[str, Any]]] = []
    for i in db_stops:
        args.append((i, int(time.time()), {'calculate_lines': True}))
    with Pool(20) as p:
        output: List[IDStopResponse] = p.map(worker, args)
    logger.info('Getting journeys from live data')
    journeys: List[List[JourneyStr]] = []
    db_sections: DBSection = connection.root().sections
    db_lines: DBLine = connection.root().lines
    db_journeys: DBJourney = connection.root().journeys
    for i in output:
        journeys.append(i.get_journeys(db_sections.keys()))
    logger.info('Merging Journeys with existing data')
    for i in journeys:
        if len(i) >= 1:
            for i in i:
                for j in db_lines.values():
                    if str(j) == str(db_journeys[i].get_line()):
                        j.add_journey(i)
    logger.info('Fetched live data in ' + str(time.time() - start_time) + ' seconds.')
