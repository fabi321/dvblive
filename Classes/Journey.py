from Classes.Time import Time
from Classes.MergeableList import MergeableList
from typing import List


class Journey:
    def __init__(self, line_id: str, trias_id: str, **kwargs):
        self._line: str = line_id
        self._trias_id: str = trias_id
        self._times: MergeableList = kwargs.get('times')

    def add_time(self, time: Time):
        self._times.append(time)
        self._uniquify()

    def _uniquify(self):
        for i in range(len(self._times) - 1, 0, -1):
            if self._times.count(self._times[i]) == 2:
                self._times[self._times.index(self._times[i])] += self._times[i]
            elif self._times.count(self._times[i]) > 2:
                raise NotImplementedError('Got more than 2 Times elements from the same station at Journey')

    def add_times(self, times: MergeableList):
        self._times += times
        self._uniquify()

    def get_times(self) -> MergeableList:
        return self._times

    def get_time_for_section_id(self, section_id: str) -> Time:
        for i in self._times:
            if i.get_section_id() == section_id:
                return i

    def get_line_id(self) -> str:
        return self._line

    def override(self, other):
        if not isinstance(other, Journey):
            raise NotImplementedError('Tried to override Journey with ' + str(type(other)))
        self = other

    def __str__(self) -> str:
        return self._trias_id

    def __eq__(self, other):
        if not isinstance(other, (Journey, str)):
            raise NotImplementedError('Tried to compare Journey with ' + str(type(other)))
        return self.__str__() == str(other)

    def __add__(self, other):
        if not isinstance(other, Journey):
            raise NotImplementedError('Tried to add Journey with ' + str(type(other)))
        if self != other:
            raise NotImplementedError('Tried to add ' + self.__str__() + ' with ' + str(other))
        self.add_times(other.get_times())
        other.override(self)
        return self

