from typing import List
from xml.etree import ElementTree

import ZODB.DB
import ZODB.config
from ZODB.Connection import Connection
from elementpath import select

from Classes.BaseTypes.StopWithoutLine import StopWithoutLine
from Classes.DBManager.DBStopWithoutLine import DBStopWithoutLine
from Classes.LowRequests.Response import Response
from Classes.Utilities import XPaths
from Classes.Utilities.db_config import zodb_conf
from Classes.Utilities.typings import StopWithoutLineStr


class StopNameResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._stop: [StopWithoutLineStr, None] = None

    def _get_stop(self):
        # TODO: use complex xpath
        ref = StopWithoutLineStr(select(self._elements, XPaths.stop_name_ref, namespaces=self._namespaces))
        db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
        connection: Connection = db.open()
        stops_without_line: DBStopWithoutLine = connection.root().stops_without_line
        if ref not in stops_without_line.keys():
            name = select(self._elements, XPaths.stop_name_name, namespaces=self._namespaces)
            stops_without_line[ref] = StopWithoutLine(ref, name)
        if not stops_without_line[ref].has_location():
            lat = select(self._elements, XPaths.stop_name_lat, namespaces=self._namespaces)
            lon = select(self._elements, XPaths.stop_name_lon, namespaces=self._namespaces)
            stops_without_line[ref].set_location({'latitude': lat, 'longitude': lon})
        self._stop = ref

    def get_stop(self) -> StopWithoutLineStr:
        if not self._stop:
            self._get_stop()
        return self._stop
