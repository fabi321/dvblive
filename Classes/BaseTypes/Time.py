import datetime

from persistent import Persistent
from transaction import commit

from Classes.Utilities.typings import SectionStr, JourneyStr, ISOTimeStr, UnixTime, StopWithoutLineStr, TimeStr


def unix_time_from_time_string(time_string: ISOTimeStr) -> UnixTime:
    time_string: str = time_string.replace('Z', '+00:00')
    time: datetime.datetime = datetime.datetime.fromisoformat(time_string)
    return UnixTime(int(time.timestamp()))


class Time(Persistent):
    def __init__(self, stop: StopWithoutLineStr, journey: JourneyStr, est_time: ISOTimeStr, plan_time: ISOTimeStr,
                 section: SectionStr):
        self._stop: StopWithoutLineStr = stop
        self._journey: JourneyStr = journey
        self._section: SectionStr = section
        self._estimated: UnixTime = unix_time_from_time_string(est_time)
        self._planned: UnixTime = unix_time_from_time_string(plan_time)
        commit()

    def get_difference(self) -> UnixTime:
        return UnixTime(self._estimated - self._planned)

    def get_estimated(self) -> UnixTime:
        return self._estimated

    def get_planned(self) -> UnixTime:
        return self._planned

    def get_section_id(self) -> SectionStr:
        return self._section

    def override(self, other):
        if not isinstance(other, Time):
            raise NotImplementedError('Tried to override Times with ' + str(type(other)))
        self = other
        commit()

    def __str__(self) -> TimeStr:
        return TimeStr(self._section + '=|=' + self._journey)

    def get_stop(self) -> StopWithoutLineStr:
        return self._stop

    def get_journey(self) -> JourneyStr:
        return self._journey

    def __eq__(self, other) -> bool:
        if not isinstance(other, (Time, str)):
            raise NotImplementedError('Tried to compare Times with ' + str(type(other)))
        return self.__str__() == str(other)

    def __add__(self, other):
        if not isinstance(other, Time):
            raise NotImplementedError('Tried to add Times with ' + str(type(other)))
        if self != other:
            raise NotImplementedError('Tried to merge ' + self.__str__() + ' with ' + str(other))
        self._planned = other.get_planned()
        self._estimated = other.get_estimated()
        other.override(self)
        return self
