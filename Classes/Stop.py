from typing import List
from Classes.Line import Line
from Classes.StopWithoutLine import StopWithoutLine
from Classes.MergeableList import MergeableList


class Stop(StopWithoutLine):
    def __init__(self, stop_id: str, line: MergeableList, name: str):
        StopWithoutLine.__init__(self, stop_id, name)
        self._line: MergeableList = line
        self._base_stop: [Stop, None] = None

    def get_lines(self) -> MergeableList:
        return self._line

    def unique_lines(self):
        list_set = set(self._line)
        self._line = list(list_set)

    def __add__(self, other):
        if not isinstance(other, Stop):
            raise NotImplementedError("Tried to add a Stop with " + str(type(other)))
#        if str(other) != self.__str__():
#            raise NotImplementedError("Tried to merge different stops")
        self._line += other.get_lines()
        if not self.has_location() and other.has_location():
            self.set_location(other.get_location())
        other.override(self)
        return self

    def _get_base_stop(self):
        stop_list: List[str] = self._stop_id.split(':')
        stop_string: str = stop_list[0] + ':' + stop_list[1] + ':' + stop_list[2]
        self._base_stop = Stop(stop_string, self._line, self._name)

    def get_base_stop(self):
        if not self._base_stop:
            self._get_base_stop()
        return self._base_stop

    def __eq__(self, other):
        if not isinstance(other, (Stop, str)):
            raise NotImplementedError("Tried to compare Stop with " + str(type(other)))
        return self.__str__() == other.__str__()
