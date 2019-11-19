from typing import List
from xml.etree import ElementTree
from elementpath import select
import XPaths
from XPaths import construct_xpath
from Classes import Location
from Classes.Line import Line
from Classes.Response import Response
from Classes.Stop import Stop
from Classes.Section import Section
import logging

logger: logging.Logger = logging.getLogger('TripResponse')


class TripResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], dictionary: bool = False, line_trias_id: str = None):
        Response.__init__(self, elements, dictionary)
        self._locations: [List[Location], None] = None
        self._ready_stops: [List[Stop], None] = None
        self._stops: [List[str], None] = None
        self._line: [Line, None] = None
        self._sections: [List[Section], None] = None
        self._lons: [List[str], None] = None
        self._lats: [List[str], None] = None
        self._predefined_line_trias_id = line_trias_id

    def _get_cords(self):
        if self._predefined_line_trias_id:
            lineref = True
        else:
            lineref = False
        lats = construct_xpath(True, lineref, True, XPaths.lats)
        lons = construct_xpath(True, lineref, True, XPaths.lons)
        if lineref:
            lats = lats.replace('$LINEREF', self._predefined_line_trias_id)
            lons = lons.replace('$LINEREF', self._predefined_line_trias_id)
        self._lons: List[str] = select(self._elements, lats, namespaces=self._namespaces)
        self._lats: List[str] = select(self._elements, lons, namespaces=self._namespaces)
        self._locations: List[Location] = []
        for i in range(len(self._lons)):
            self._locations.append({'latitude': float(self._lats[i]), 'longitude': float(self._lons[i])})
        for i in range(len(self._locations) - 1, 1, -1):
            if self._locations.count(self._locations[i]) > 1:
                self._locations.pop(i)


    def get_cords(self) -> List[Location]:
        if not self._locations:
            self._get_cords()
        return self._locations

    def _get_line(self):
        if self._predefined_line_trias_id:
            lineref = True
        else:
            lineref = False
        line_number: str = construct_xpath(True, lineref, True, XPaths.line_number)
        line_string: str = construct_xpath(True, lineref, True, XPaths.line_string)
        line_trias_id: str = construct_xpath(True, lineref, True, XPaths.line_trias_id)
        if lineref:
            line_number = line_number.replace('$LINEREF', self._predefined_line_trias_id)
            line_trias_id = line_trias_id.replace('$LINEREF', self._predefined_line_trias_id)
            line_string = line_string.replace('$LINEREF', self._predefined_line_trias_id)
        line_number: List[str] = select(self._elements, line_number, namespaces=self._namespaces)
        self._line_number: int = int(line_number[0]) if line_number else None
        line_string: List[str] = select(self._elements, line_string, namespaces=self._namespaces)
        self._line_string: str = line_string[0] if line_string else None
        line_trias_id: List[str] = select(self._elements, line_trias_id, namespaces=self._namespaces)
        self._line_trias_id: str = line_trias_id[0] if line_trias_id else None
        if not self._line_trias_id:
            logger.warning('Empty TripResponse')
            return
        self._line = Line(self._line_number, self._line_string, self._line_trias_id)

    def get_line(self) -> Line:
        if not self._line:
            self._get_line()
        return self._line

    def _get_stops(self):
        if self._predefined_line_trias_id:
            lineref = True
        else:
            lineref = False
        stops = construct_xpath(True, lineref, True, XPaths.stops)
        stop_names = construct_xpath(True, lineref, True, XPaths.stop_names)
        if lineref:
            stops = stops.replace('$LINEREF', self._predefined_line_trias_id)
            stop_names = stop_names.replace('$LINEREF', self._predefined_line_trias_id)
        self._stops: List[str] = select(self._elements, stops, namespaces=self._namespaces)
        self._stop_names: List[str] = select(self._elements, stop_names, namespaces=self._namespaces)

    def get_stops(self) -> List[Stop]:
        if not self._ready_stops:
            if not self._stops:
                self._get_stops()
            if not self._line:
                self._get_line()
            self._ready_stops: List[Stop] = []
            for i in range(len(self._stops)):
                self._ready_stops.append(Stop(self._stops[i], [self._line], self._stop_names[i]))
        return self._ready_stops

    def _get_sections(self):
        self._sections: List[Section] = []
        if not self._stops:
            self._get_stops()
        if not self._line:
            self._get_line()
        for i in range(1, len(self._stops)):
            self._sections.append(Section(self._ready_stops[i - 1], self._ready_stops[i], self._line))

    def get_sections(self) -> List[Section]:
        if not self._sections:
            self._get_sections()
        return self._sections
