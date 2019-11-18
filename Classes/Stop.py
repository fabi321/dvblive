from typing import List, Dict
from Classes import Location
from Classes.Line import Line
from Classes.LocationResponse import LocationResponse


class StopWithoutLine:
    def __init__(self, stop_id: str):
        self._stop_id: str = stop_id
        self._location: [Location, None] = None
        self._base_stop: [StopWithoutLine, None] = None

    def __str__(self) -> str:
        return self._stop_id

    def __eq__(self, other):
        if not isinstance(other, Stop):
            raise NotImplementedError("Tried to compare Stop with " + str(type(other)))
        return self.__str__() == other.__str__()

    def set_location(self, location: Location):
        self._location = location

    def get_location(self) -> Location:
        if not self._location:
            self._location = {'latitude': 0.0, 'longitude': 0.0}
#            raise NotImplementedError("Tried to fetch stop location while none was saved")
        return self._location

    def has_location(self) -> bool:
        return True if self._location else False

    def __get_base_stop(self):
        stop_list: List[str] = self._stop_id.split(':')
        stop_string: str = stop_list[0] + ':' + stop_list[1] + ':' + stop_list[2]
        self._base_stop = StopWithoutLine(stop_string)

    def get_base_stop(self):
        if not self._base_stop:
            self.__get_base_stop()
        return self._base_stop


class Stop(StopWithoutLine):
    def __init__(self, stop_id: str, line: List[Line]):
        StopWithoutLine.__init__(self, stop_id)
        self._line: List[Line] = line
        self._base_stop: [Stop, None] = None

    def get_lines(self) -> List[Line]:
        return self._line

    def unique_lines(self):
        list_set = set(self._line)
        self._line = list(list_set)

    def override(self, stop):
        if not isinstance(stop, Stop):
            raise NotImplementedError("Tried to override Stop with " + str(type(stop)))
        self = stop

    def __add__(self, other):
        if not isinstance(other, Stop):
            raise NotImplementedError("Tried to add a Stop with " + str(type(other)))
#        if str(other) != self.__str__():
#            raise NotImplementedError("Tried to merge different stops")
        self._line += other.get_lines()
        other.override(self)
        return self

    def __get_base_stop(self):
        stop_list: List[str] = self._stop_id.split(':')
        stop_string: str = stop_list[0] + ':' + stop_list[1] + ':' + stop_list[2]
        self._base_stop = Stop(stop_string, self._line)

    def get_base_stop(self):
        if not self._base_stop:
            self.__get_base_stop()
        return self._base_stop
