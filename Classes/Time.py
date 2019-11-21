from Classes.StopWithoutLine import StopWithoutLine
import datetime


def unix_time_from_time_string(time_string: str) -> int:
    time_string: str = time_string.replace('Z', '+00:00')
    time: datetime.datetime = datetime.datetime.fromisoformat(time_string)
    return int(time.timestamp())


class Time:
    def __init__(self, stop: StopWithoutLine, est_time: str, plan_time: str):
        self._stop: StopWithoutLine = stop
        self._estimated: int = unix_time_from_time_string(est_time)
        self._planned: int = unix_time_from_time_string(plan_time)

    def get_difference(self) -> int:
        return self._estimated - self._planned

    def get_estimated(self) -> int:
        return self._estimated

    def get_planned(self) -> int:
        return self._planned

    def override(self, other):
        if not isinstance(other, Time):
            raise NotImplementedError('Tried to override Times with ' + str(type(other)))
        self = other

    def __str__(self) -> str:
        return str(self._stop)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Time):
            raise NotImplementedError('Tried to compare Times with ' + str(type(other)))
        return self.__str__() == str(other)

    def __add__(self, other):
        if not isinstance(other, Time):
            raise NotImplementedError('Tried to add Times with ' + str(type(other)))
        self._planned = other.get_planned()
        self._estimated = other.get_estimated()
        other.override(self)
        return self
