from typing import List
from xml.etree import ElementTree

from elementpath import select

from Classes.LowRequests.Response import Response
from Classes.Utilities import XPaths
from Classes.Utilities.typings import Location


class LocationResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._lat: [float, None] = None

    def _get_cords(self):
        # TODO: Use complex Xpaths
        lat = select(self._elements, XPaths.location_lat, namespaces=self._namespaces)
        self._lat: float = float(lat[0]) if lat else None
        lon = select(self._elements, XPaths.location_lon, namespaces=self._namespaces)
        self._lon: float = float(lon[0]) if lon else None

    def get_cords(self) -> Location:
        if not self._lat:
            self._get_cords()
        return {'latitude': self._lat, 'longitude': self._lon}
