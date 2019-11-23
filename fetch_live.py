from fetch_init import output_format
from Classes.IDStopResponse import IDStopResponse
from Classes.StopWithoutLine import StopWithoutLine
from Classes.Journey import Journey
from Classes.MergeableList import MergeableList
from typing import List, Any, Tuple, Dict
import time
from multiprocessing import Pool


def worker(args_kwargs: Tuple[Any, int, Dict[str, Any]]):
    return IDStopResponse(args_kwargs[0], args_kwargs[1], **args_kwargs[2])


def fetch_live(init_data: output_format) -> output_format:
    args: List[Tuple[Any, int, Dict[str, Any]]] = []
    for i in init_data[1]:
        args.append((i, int(time.time()), {'calculate_lines': True}))
    with Pool(20) as p:
        output: MergeableList = MergeableList(p.map(worker, args))
    journeys: List[List[Journey]] = []
    for i in output:
        journeys.append(i.get_journeys(init_data[2]))
    for i in journeys:
        if len(i) >= 1:
            for i in i:
                for j in init_data[0]:
                    if str(j) == str(i.get_line_id()):
                        j.add_journey(i)
    return init_data
