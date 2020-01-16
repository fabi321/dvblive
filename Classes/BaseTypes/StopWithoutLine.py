from typing import List

import ZODB.DB
import ZODB.config
from ZODB.Connection import Connection
from persistent import Persistent
from transaction import commit

from Classes.Utilities.db_config import zodb_conf
# from Classes.DBManager.DBStopWithoutLine import DBStopWithoutLine
from Classes.Utilities.typings import StopWithoutLineStr, Location


class StopWithoutLine(Persistent):
    def __init__(self, stop_id: StopWithoutLineStr, name: str):
        self._stop_id: StopWithoutLineStr = stop_id
        self._name: str = name
        self._location: [Location, None] = None
        self._base_stop: [StopWithoutLineStr, None] = None
        commit()

    def override(self, stop):
        if not isinstance(stop, StopWithoutLine):
            raise NotImplementedError("Tried to override Stop with " + str(type(stop)))
        self = stop
        commit()

    def __str__(self) -> StopWithoutLineStr:
        return self._stop_id

    def __eq__(self, other):
        if not isinstance(other, (StopWithoutLine, str, StopWithoutLineStr)):
            raise NotImplementedError("Tried to compare Stop with " + str(type(other)))
        return self.__str__() == other.__str__()

    def __add__(self, other):
        if not isinstance(other, StopWithoutLine):
            raise NotImplementedError("Tried to add a StopWithoutLocation with " + str(type(other)))
        if str(other) != self.__str__():
            raise NotImplementedError("Tried to merge different stops")
        if not self.has_location() and other.has_location():
            self.set_location(other.get_location())
        commit()
        other.override(self)
        return self

    def set_location(self, location: Location):
        self._location = location

    def get_location(self) -> Location:
        if not self._location:
            self._location = {'latitude': 0.0, 'longitude': 0.0}
        #            raise NotImplementedError("Tried to fetch stop location while none was saved")
        return self._location

    def has_location(self) -> bool:
        return True if self._location else False

    def _get_base_stop(self):
        stop_list: List[str] = self._stop_id.split(':')
        self._base_stop: StopWithoutLineStr = StopWithoutLineStr(stop_list[0] + ':' + stop_list[1] + ':' + stop_list[2])
        db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
        connection: Connection = db.open()
        #        stops: DBStopWithoutLine = connection.root().stops_without_line
        stops = connection.root().stops_without_line
        if self._base_stop not in stops.keys():
            stops[self._base_stop] = StopWithoutLine(self._base_stop, self._name)
        commit()
        connection.close()
        db.close()

    def get_base_stop(self):
        if not self._base_stop:
            self._get_base_stop()
        return self._base_stop
