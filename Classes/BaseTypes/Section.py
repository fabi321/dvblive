from typing import List

import ZODB.DB
import ZODB.config
from ZODB.Connection import Connection
from persistent import Persistent
from persistent.list import PersistentList
from transaction import commit

from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import LineStr, StopStr, SectionStr, Location


class Section(Persistent):
    def __init__(self, start_stop: StopStr, end_stop: StopStr, line: LineStr):
        self._start_stop: StopStr = start_stop
        self._end_stop: StopStr = end_stop
        self._line: PersistentList[LineStr] = PersistentList([line])
        self._polygon: PersistentList = PersistentList()
        commit()

    def __str__(self) -> SectionStr:
        return SectionStr(self._start_stop + '=|=' + self._end_stop)

    def get_lines(self) -> List[LineStr]:
        return list(self._line)

    def add_line(self, line: LineStr):
        self._line.append(line)
        commit()

    def set_polygon(self, polygon: List[Location]):
        self._polygon = PersistentList(polygon)
        commit()

    def __eq__(self, other):
        if not isinstance(other, (Section, str, SectionStr)):
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

    def get_polygon(self) -> List[Location]:
        if not self._polygon:
            db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
            connection: Connection = db.open()
            stops = connection.root().stops
            polygons: List[Location] = [stops[self._start_stop].get_location(), stops[self._end_stop].get_location()]
            connection.close()
            db.close()
            return polygons
        return self._polygon

    def get_start_stop(self) -> StopStr:
        return self._start_stop

    def get_end_stop(self) -> StopStr:
        return self._end_stop

    def override(self, section):
        if not isinstance(section, Section):
            raise NotImplementedError('Tried to override section with ' + str(type(section)))
        self = section
        commit()
