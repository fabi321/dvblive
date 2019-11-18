from typing import List
from xml.etree import ElementTree
from elementpath import select
import XPaths
from Classes import Location
from Classes.Line import Line
from Classes.Response import Response
from Classes.Stop import Stop
from Classes.Section import Section


class TripResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], dictionary: bool = False):
        Response.__init__(self, elements, dictionary)
        self._locations: [List[Location], None] = None
        self._ready_stops: [List[Stop], None] = None
        self._stops: [List[str], None] = None
        self._line: [Line, None] = None
        self._sections: [List[Section], None] = None
        self._lons: [List[str], None] = None
        self._lats: [List[str], None] = None

    def __get_cords(self):
        self._lons: List[str] = select(self._elements, XPaths.lats, namespaces=self._namespaces)#TODO Lineref, Lines
        self._lats: List[str] = select(self._elements, XPaths.lons, namespaces=self._namespaces)
        self._locations: List[Location] = []
        for i in range(len(self._lons)):
            self._locations.append({'latitude': float(self._lats[i]), 'longitude': float(self._lons[i])})
        for i in range(len(self._locations) - 1, 1, -1):
            if self._locations.count(self._locations[i]) > 1:
                self._locations.pop(i)


    def get_cords(self) -> List[Location]:
        if not self._locations:
            self.__get_cords()
        return self._locations

    def __get_stops(self):
        self._stops: List[str] = select(self._elements, XPaths.stops, namespaces=self._namespaces)

    def __get_line(self):
        line_number: str = select(self._elements, XPaths.line_number, namespaces=self._namespaces)
        self._line_number: int = int(line_number[0]) if line_number else None
        line_string = select(self._elements, XPaths.line_string, namespaces=self._namespaces)
        self._line_string: str = line_string[0] if line_string else None
        line_trias_id = select(self._elements, XPaths.line_trias_id, namespaces=self._namespaces)
        self._line_trias_id: str = line_trias_id[0] if line_trias_id else None
        self._line = Line(self._line_number, self._line_string, self._line_trias_id)

    def get_stops(self) -> List[Stop]:
        if not self._ready_stops:
            if not self._stops:
                self.__get_stops()
            if not self._line:
                self.__get_line()
            self._ready_stops: List[Stop] = []
            for i in self._stops:
                self._ready_stops.append(Stop(i, [self._line]))
        return self._ready_stops

    def __get_sections(self):
        self._sections: List[Section] = []
        if not self._stops:
            self.__get_stops()
        if not self._line:
            self.__get_line()
        for i in range(1, len(self._stops)):
            self._sections.append(Section(self._ready_stops[i - 1], self._ready_stops[i], self._line))

    def get_sections(self) -> List[Section]:
        if not self._sections:
            self.__get_sections()
        return self._sections

    def get_line(self) -> Line:
        if not self._line:
            self.__get_line()
        return self._line