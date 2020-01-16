import datetime
import logging
import time
from typing import List, Tuple, Any

import ZODB.config
from ZODB.Connection import Connection

from Classes.BaseTypes.Line import Line
from Classes.DBManager.DBLine import DBLine
from Classes.DBManager.DBSection import DBSection
from Classes.DBManager.DBStop import DBStop
from Classes.LowRequests.TripResponse import TripResponse
from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.request import parallel_location, parallel_stop, parallel_trip
from Classes.Utilities.typings import *

logger: logging.Logger = logging.getLogger('fetch_init')

db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)


def fetch_init(debug: bool = False):
    connection: Connection = db.open()
    logger.info('Fetching init data')
    start_time: float = time.time()
    request_parallelization: int = 20
    if debug:
        request_parallelization: int = 1
    request_time: datetime.datetime = datetime.datetime.now()
    request_time: datetime.datetime = request_time.replace(hour=12, minute=0, second=0)
    request_time: UnixTime = UnixTime(int(request_time.timestamp()))
    base_stops: List[StopWithoutLineStr] = [StopWithoutLineStr('de:14612:13'), StopWithoutLineStr('de:14612:5'),
                                            StopWithoutLineStr('de:14612:7')]
    base_dicts: List[Tuple[StopWithoutLineStr, UnixTime, int]] = []
    for i in base_stops:
        base_dicts.append((i, request_time, 15))
    logger.info('Getting lines from base stops.')
    parallel_stop(base_dicts, debug=debug, threads=request_parallelization, calculate_lines=True)
    db_lines: DBLine = connection.root().lines
    logger.info('Got ' + str(len(db_lines)) + ' lines.')
    trips: List[Tuple[StopWithoutLineStr, StopWithoutLineStr, UnixTime]] = []
    kwargs: List[Dict[str, Any]] = []
    for i, j in db_lines:
        trips.append((j.get_stops()[0], j.get_stops()[1], request_time))
        kwargs.append({'line_trias_id': i, 'debug': debug, 'calculate_stops': True, 'calculate_sections': True})
    logger.info('Getting lines from start and end stops.')
    lines: List[TripResponse] = parallel_trip(trips, debug=debug, threads=request_parallelization, kwargs=kwargs)
    db_stops: DBStop = connection.root().stops
    for i in lines:
        line: Line = db_lines[i.get_line()]
        for i in i.get_stops():
            base_stop: StopStr = db_stops[i].get_base_stop()
            line.add_stop(i)
    logger.info('Got ' + str(len(db_stops)) + ' Stops from lines')
    logger.info('Getting locations for stops')
    parallel_location(db_stops.keys())
    logger.info('Got locations for ' + str(len(db_stops)) + ' stops')
    #    logger.info('Uniquifying lines in stops')
    #    for i in unique_stops:
    #        i.unique_lines()
    db_sections: DBSection = connection.root().sections
    logger.info('Got ' + str(len(db_sections)) + ' sections.')
    trips: List[Tuple[StopWithoutLineStr, StopWithoutLineStr, UnixTime]] = []
    kwargs: List[Dict[str, Any]] = []
    for i, j in db_sections:
        if j.get_lines():
            trips.append((i.get_start_stop(), i.get_end_stop(),
                          request_time))
            kwargs.append({'debug': debug, 'id': str(i), 'polygons': True, 'line_trias_id': str(i.get_lines()[0])})
    logger.info('Getting polygons for section')
    polygons: List[TripResponse] = parallel_trip(trips, threads=request_parallelization * 2, kwargs=kwargs)
    logger.info('Got polygons for ' + str(len(db_sections)) + ' sections.')
    logger.info('Apylying polygons to sections')
    for i in polygons:
        db_sections[i.get_sections()[0]].set_polygon(i.get_cords())
    logger.info('Applied polygons to sections')
    logger.info('Fetched init_data in ' + str(int(time.time() - start_time)) + ' seconds.')
    connection.close()
