from typing import List
from Classes.MergeableList import MergeableList
from Classes.StopWithoutLine import StopWithoutLine
from Classes.Journey import Journey
from Classes.Time import Time

class Line:
    def __init__(self, number: int, string: str, trias_id: str):
        self._number: int = number
        self._string: str = string
        self._trias_id: str = trias_id
        assert type(self._trias_id) == str
        self._stops: [MergeableList, None] = None
        self._journeys: List[Journey] = []

    def __str__(self) -> str:
        return self._trias_id

    def add_stop(self, stop: StopWithoutLine):
        if not self._stops:
            self._stops = [stop]
        else:
            self._stops.append(stop)

    def get_stops(self) -> MergeableList:
        return self._stops

    def add_journey(self, journey: Journey):
        try:
            self._journeys[self._journeys.index(journey)] += journey
        except ValueError:
            self._journeys.append(journey)

    def get_journeys_for_section_id(self, section_id: str) -> List[Time]:
        out: List[Time] = []
        for i in self._journeys:
            tmp: Time = i.get_time_for_section_id(section_id)
            if tmp:
                out.append(tmp)
        return out

    def delete_stops(self):
        self._stops.clear()

    def get_line_number(self) -> int:
        return self._number
