import time
from multiprocessing import Pool
from typing import List, Any, Tuple, Dict

from Classes.BaseTypes.Journey import Journey
from Classes.HighRequests.IDStopResponse import IDStopResponse
from Classes.MergeableList import MergeableList
import logging

logger: logging.Logger = logging.getLogger('fetch_live')


def worker(args_kwargs: Tuple[Any, int, Dict[str, Any]]):
    return IDStopResponse(args_kwargs[0], args_kwargs[1], **args_kwargs[2])


def fetch_live():
    start_time: int = time.time()
    logger.info('Fetching live data')
    args: List[Tuple[Any, int, Dict[str, Any]]] = []
    for i in init_data[1]:
        args.append((i, int(time.time()), {'calculate_lines': True}))
    with Pool(20) as p:
        output: MergeableList[IDStopResponse] = MergeableList(p.map(worker, args))
    logger.info('Getting journeys from live data')
    journeys: List[List[Journey]] = []
    for i in output:
        journeys.append(i.get_journeys(init_data[2]))
    logger.info('Merging Journeys with existing data')
    for i in journeys:
        if len(i) >= 1:
            for i in i:
                for j in init_data[0]:
                    if str(j) == str(i.get_line()):
                        j.add_journey(i)
    logger.info('Fetched live data in ' + str(time.time() - start_time) + ' seconds.')
    return init_data
