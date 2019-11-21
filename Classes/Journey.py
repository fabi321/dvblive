from Classes.Line import Line
from Classes.Time import Time
from typing import List


class Journey:
    def __init__(self, line: Line, trias_id: str, **kwargs):
        self._line: Line = line
        self._trias_id: str = trias_id
        self._times: List[Time] = kwargs.get('times')

    def add_time(self, time: Time):
        self._times.append(time)

    def _uniquify(self):
        for i in range(len(self._times) - 1, 0, -1):
            if self._times.count(self._times[i]) == 2:
                self._times[self._times.index(self._times[i])] += self._times[i]
            elif self._times.count(self._times[i]) > 2:
                raise NotImplementedError('Got more than 2 Times elements from the same station at Journey')

    def add_times(self, times: List[Time]):
        self._times += times
        self._uniquify()

    def get_times(self) -> List[Time]:
        return self._times
