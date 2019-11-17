from typing import List, Dict
from Classes import Location
from Classes.Line import Line
from Classes.LocationResponse import LocationResponse


class StationWithoutLine:
    def __init__(self, station_id: str):
        self._station_id: str = station_id
        self._location: [Location, None] = None


    def __str__(self) -> str:
        return self._station_id

    def __eq__(self, other):
        if not isinstance(other, Station):
            raise NotImplementedError("Tried to compare Station with " + type(other))
        return self.__str__() == other.__str__()

    def set_location(self, location: Location):
        self._location = location

    def get_location(self) -> Location:
        if not self._location:
            self._location = {'latitude': 0.0, 'longitude': 0.0}
#            raise NotImplementedError("Tried to fetch station location while none was saved")
        return self._location

    def has_location(self) -> bool:
        return True if self._location else False


class Station(StationWithoutLine):
    def __init__(self, station_id: str, line: Line):
        StationWithoutLine.__init__(self, station_id)
        self._line: List[Line] = [line]

    def get_lines(self) -> List[Line]:
        return self._line

    def unique_lines(self):
        list_set = set(self._line)
        self._line = list(list_set)

    def override(self, station):
        if not isinstance(station, Station):
            raise NotImplementedError("Tried to override Station with " + type(station))
        self = station

    def __add__(self, other):
        if not isinstance(other, Station):
            raise NotImplementedError("Tried to add a Station with " + type(other))
        if str(other) != self.__str__():
            raise NotImplementedError("Tried to merge different stations")
        self._line += other.get_lines()
        other.override(self)
        return self
