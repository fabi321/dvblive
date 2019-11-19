from Classes.Response import Response
from Classes.StopWithoutLine import StopWithoutLine
from typing import List
from xml.etree import ElementTree
from elementpath import select
import XPaths


class StopNameResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], dictionary: bool = False):
        Response.__init__(self, elements, dictionary)
        self._stop: [StopWithoutLine, None] = None

    def _get_stop(self):
        name = select(self._elements, XPaths.stop_name_name, namespaces=self._namespaces)
        ref = select(self._elements, XPaths.stop_name_ref, namespaces=self._namespaces)
        lat = select(self._elements, XPaths.stop_name_lat, namespaces=self._namespaces)
        lon = select(self._elements, XPaths.stop_name_lon, namespaces=self._namespaces)
        self._stop = StopWithoutLine(ref, name)
        self._stop.set_location({'latitude': lat, 'longitude': lon})

    def get_stop(self) -> StopWithoutLine:
        if not self._stop:
            self._get_stop()
        return self._stop
