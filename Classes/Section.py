from typing import List
from Classes import Location
from Classes.Line import Line
from Classes.Stop import Stop
from Classes.MergeableList import MergeableList


class Section:
    def __init__(self, start_stop: Stop, end_stop: Stop, line: Line):
        self._start_stop: Stop = start_stop
        self._end_stop: Stop = end_stop
        self._line: MergeableList = MergeableList([line])
        self._polygon: [MergeableList, None] = None

    def __str__(self) -> str:
        return str(self._start_stop) + '=|=' + str(self._end_stop)

    def get_lines(self) -> MergeableList:
        return self._line

    def set_polygon(self, polygon: MergeableList):
        self._polygon = polygon

    def __eq__(self, other):
        if not isinstance(other, (Section, str)):
            raise NotImplementedError("Tried to compare Section with " + str(type(other)))
        return self.__str__() == other.__str__()

    def __add__(self, other):
        if not isinstance(other, Section):
            raise NotImplementedError("Tried to add Section and " + str(type(other)))
        if other != self:
            raise NotImplementedError("Tried to merge different sections")
        self._line += other.get_lines()
        other.override(self)
        return self

    def get_polygon(self) -> MergeableList:
        if not self._polygon:
            self._polygon: MergeableList = MergeableList([self._start_stop.get_location(), self._end_stop.get_location()])
        return self._polygon

    def get_start_stop(self) -> Stop:
        return self._start_stop

    def get_end_stop(self) -> Stop:
        return self._end_stop

    def override(self, section):
        if not isinstance(section, Section):
            raise NotImplementedError('Tried to override section with ' + str(type(section)))
        self = section
