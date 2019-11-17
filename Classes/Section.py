from typing import List
from Classes import Location
from Classes.Line import Line
from Classes.Station import Station


class Section:
    def __init__(self, start_station: Station, end_station: Station, line: Line):
        self._start_station: Station = start_station
        self._end_station: Station = end_station
        self._line: List[Line] = [line]
        self._polygon: [List[Location], None] = None

    def __str__(self) -> str:
        return str(self._start_station) + '=|=' + str(self._end_station)

    def get_lines(self) -> List[Line]:
        return self._line

    def __add__(self, other):
        if not isinstance(other, Section):
            raise NotImplementedError("Tried to add Section and " + type(other))
        if str(other) != self.__str__():
            raise NotImplementedError("Tried to merge different sections")
        self._line += other.get_lines()
        other.override(self)
        return self

    def set_polygon(self, polygon: List[Location]):
        self._polygon = polygon

    def __eq__(self, other):
        if not isinstance(other, Section):
            raise NotImplementedError("Tried to compare Section with " + type(other))
        return self.__str__() == other.__str__()

    def get_polygon(self) -> List[Location]:
        if not self._polygon:
            self._polygon = [self._start_station.get_location(), self._end_station.get_location()]
        return self._polygon

    def get_start_station(self) -> Station:
        return self._start_station

    def get_end_station(self) -> Station:
        return self._end_station

    def override(self, section):
        if not isinstance(section, Section):
            raise NotImplementedError('Tried to override section with ' + type(section))
        self = section
