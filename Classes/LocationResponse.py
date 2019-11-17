from typing import List
from xml.etree import ElementTree
from elementpath import select
import XPaths
from Classes import Location
from Classes.Response import Response


class LocationResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], dictionary: bool = False):
        Response.__init__(self, elements, dictionary)
        self._lat: [float, None] = None

    def __get_cords(self):
        lat = select(self._elements, XPaths.lat, namespaces=self._namespaces)
        self._lat: float = float(lat[0]) if lat else None
        lon = select(self._elements, XPaths.lon, namespaces=self._namespaces)
        self._lon: float = float(lon[0]) if lon else None

    def get_cords(self) -> Location:
        if not self._lat:
            self.__get_cords()
        return {'latitude': self._lat, 'longitude': self._lon}