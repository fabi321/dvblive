from typing import List, Union

import ZODB.DB
import ZODB.config
from ZODB.Connection import Connection
from persistent import Persistent
from persistent.list import PersistentList
from transaction import commit

from Classes.BaseTypes.Time import Time
from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import StopWithoutLineStr, JourneyStr, TimeStr, LineStr, SectionStr, StopStr


class Line(Persistent):
    def __init__(self, number: int, string: str, trias_id: LineStr):
        self._number: int = number
        self._string: str = string
        self._trias_id: LineStr = trias_id
        self._stops: PersistentList[Union[StopWithoutLineStr, StopStr]] = PersistentList()
        self._journeys: PersistentList[JourneyStr] = PersistentList()
        commit()

    def __str__(self) -> LineStr:
        return self._trias_id

    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, (Line, str, LineStr)):
            raise NotImplementedError('Tried to compare Line with ' + str(type(other)))
        return self.__str__() == str(other)

    def add_stop(self, stop: [StopWithoutLineStr, StopStr]):
        self._stops.append(stop)
        commit()

    def get_stops(self) -> List[Union[StopWithoutLineStr, StopStr]]:
        return list(self._stops)

    def add_journey(self, journey: JourneyStr):
        try:
            self._journeys.index(journey)
        #            raise NotImplementedError('Old, fucked up Behavior, tried to add already exsisting journey to line')
        except ValueError:
            self._journeys.append(journey)
        commit()

    def get_times_for_section_id(self, section_id: SectionStr) -> List[TimeStr]:
        db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
        connection: Connection = db.open()
        journeys = connection.root().journeys
        out: List[TimeStr] = []
        for i in self._journeys:
            tmp: Time = journeys[i].get_time_for_section_id(section_id)
            if tmp:
                out.append(i)
        connection.close()
        db.close()
        return out

    def delete_stops(self):
        self._stops.clear()
        commit()

    def get_line_number(self) -> int:
        return self._number

    def get_len_stops(self) -> int:
        if not self._stops:
            return 0
        return len(self._stops)

    def override(self, other):
        if not isinstance(other, Line):
            raise NotImplementedError('Tried to override Line with ' + str(type(other)))
        self = other
        commit()

    def __add__(self, other):
        if not isinstance(other, Line):
            raise NotImplementedError('Tried to add Line with ' + str(type(other)))
        if self != other:
            raise NotImplementedError('Tried to add Line ' + str(self) + ' with ' + str(other))
        if self.get_len_stops() < other.get_len_stops():
            for i in other.get_stops():
                self.add_stop(i)
        other.override(self)
