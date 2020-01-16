from typing import List

import ZODB.DB
import ZODB.config
from ZODB.Connection import Connection
from persistent.list import PersistentList
from transaction import commit

from Classes.BaseTypes.StopWithoutLine import StopWithoutLine
from Classes.Utilities.db_config import zodb_conf
# from Classes.DBManager.DBStop import DBStop
from Classes.Utilities.typings import LineStr, StopStr


class Stop(StopWithoutLine):
    def __init__(self, stop_id: StopStr, line: List[LineStr], name: str):
        StopWithoutLine.__init__(self, stop_id, name)
        self._line: PersistentList = PersistentList()
        for i in line:
            if i:
                self._line.append(i)
        self._base_stop: [StopStr, None] = None
        commit()

    def get_lines(self) -> List[LineStr]:
        return self._line

    def add_line(self, line: LineStr):
        self._line.append(line)
        commit()

    def unique_lines(self):
        for i in range(len(self._line) - 1, 0, -1):
            if self._line[i]:
                if self._line.count(self._line[i]) > 1:
                    # self._line[self._line.index(self._line[i])] += self._line[i]
                    self._line.pop(i)
        commit()

    def __add__(self, other):
        if not isinstance(other, Stop):
            raise NotImplementedError("Tried to add a Stop with " + str(type(other)))
        if str(other) != self.__str__():
            raise NotImplementedError("Tried to merge different stops")
        for i in other.get_lines():
            if i:
                if self._line.count(i) >= 1:
                    self._line[self._line.index(i)] += i
                else:
                    self._line.append(i)
        if not self.has_location() and other.has_location():
            self.set_location(other.get_location())
        commit()
        other.override(self)
        return self

    def _get_base_stop(self):
        stop_list: List[str] = self._stop_id.split(':')
        self._base_stop: StopStr = StopStr(stop_list[0] + ':' + stop_list[1] + ':' + stop_list[2])
        db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
        connection: Connection = db.open()
        #        stops: DBStop = connection.root().stops
        stops = connection.root().stops
        if self._base_stop not in stops.keys():
            stops[self._base_stop] = Stop(self._base_stop, self._line, self._name)
        commit()
        connection.close()
        db.close()

    def get_base_stop(self):
        if not self._base_stop:
            self._get_base_stop()
        return self._base_stop

    def __eq__(self, other):
        if not isinstance(other, (Stop, str)):
            raise NotImplementedError("Tried to compare Stop with " + str(type(other)))
        return self.__str__() == other.__str__()

    def get_name(self) -> str:
        return self._name

    def update_stop_without_line(self):
        db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
        connection: Connection = db.open()
        stops_without_line = connection.root().stops_without_line
        full_stop: StopWithoutLine = stops_without_line[self._stop_id]
        self.override(full_stop)
        connection.close()
        db.close()
