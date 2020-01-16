from typing import List

import ZODB.DB
import ZODB.config
from ZODB.Connection import Connection
from persistent import Persistent
from persistent.list import PersistentList
from transaction import commit

from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import LineStr, TimeStr, JourneyStr


class Journey(Persistent):
    def __init__(self, line: LineStr, trias_id: JourneyStr, **kwargs):
        self._line: LineStr = line
        self._trias_id: JourneyStr = trias_id
        self._times: PersistentList[TimeStr] = PersistentList(kwargs.get('times'))
        commit()

    def _uniquify(self):
        for i in range(len(self._times) - 1, 0, -1):
            if self._times.count(self._times[i]) > 1:
                self._times.pop(i)
        commit()

    #                self._times[self._times.index(self._times[i])] += self._times[i]
    #            elif self._times.count(self._times[i]) > 2:
    #                raise NotImplementedError('Got more than 2 Times elements from the same station at Journey')

    def add_time(self, time: TimeStr):
        self._times.append(time)
        self._uniquify()

    def add_times(self, times: List[TimeStr]):
        self._times += PersistentList(times)
        self._uniquify()

    def get_times(self) -> List[TimeStr]:
        return list(self._times)

    def get_time_for_section_id(self, section_id: str) -> TimeStr:
        db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
        connection: Connection = db.open()
        sections = connection.root().sections
        for i in self._times:
            if sections[i].get_section_id() == section_id:
                connection.close()
                db.close()
                return i
        connection.close()
        db.close()

    def get_line(self) -> LineStr:
        return self._line

    def override(self, other):
        if not isinstance(other, Journey):
            raise NotImplementedError('Tried to override Journey with ' + str(type(other)))
        self = other
        commit()

    def __str__(self) -> JourneyStr:
        return self._trias_id

    def __eq__(self, other):
        if not isinstance(other, (Journey, str, JourneyStr)):
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
