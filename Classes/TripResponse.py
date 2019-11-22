from typing import List, Dict, Any
from xml.etree import ElementTree
from XPaths import construct_complex_xpath
from Classes import Location
from Classes.Line import Line
from Classes.Response import Response
from Classes.Stop import Stop
from Classes.Section import Section
import logging

logger: logging.Logger = logging.getLogger('TripResponse')


class TripResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._locations: [List[Location], None] = None
        self._ready_stops: [List[Stop], None] = None
        self._stops: [List[str], None] = None
        self._line: [Line, None] = None
        self._sections: [List[Section], None] = None
        self._lons: [List[str], None] = None
        self._lats: [List[str], None] = None
        self._predefined_line_trias_id = kwargs.get('line_trias_id')
        self._kwargs: Dict[str, Any] = {'tree': self._elements, 'namespaces': self._namespaces}
        if self._predefined_line_trias_id:
            self._kwargs.update({'lineref': self._predefined_line_trias_id})

    def _get_cords(self):
        if self._predefined_line_trias_id:
            is_lineref = True
        else:
            is_lineref = False
        complex_string: List[str] = construct_complex_xpath('Trip', is_lineref, True, 'lats', 'lons', **self._kwargs)
        self._locations: List[Location] = []
        for i in complex_string:
            list: List[str] = i.split(' # ')
            self._locations.append({'latitude': float(list[0]), 'longitude': float(list[1])})
        for i in range(len(self._locations) - 1, 1, -1):
            if self._locations.count(self._locations[i]) > 1:
                self._locations.pop(i)


    def get_cords(self) -> List[Location]:
        if not self._locations:
            self._get_cords()
        return self._locations

    def _get_line(self):
        if self._predefined_line_trias_id:
            is_lineref = True
        else:
            is_lineref = False
        complex_string: List[str] = construct_complex_xpath('Trip', is_lineref, True, 'line_number', 'line_string', 'line_trias_id', **self._kwargs)
        if len(complex_string) >= 1:
            list: List[str] = complex_string[0].split(' # ')
            self._line_number: int = int(list[0])
            self._line_string: str = list[1]
            self._line_trias_id: str = list[2]
        else:
            logger.warning('Empty TripResponse')
            return
        self._line = Line(self._line_number, self._line_string, self._line_trias_id)

    def get_line(self) -> Line:
        if not self._line:
            self._get_line()
        return self._line

    def _get_stops(self):
        if self._predefined_line_trias_id:
            is_lineref = True
        else:
            is_lineref = False
        complex_string: List[str] = construct_complex_xpath('Trip', is_lineref, True, 'stops', 'stop_names', **self._kwargs)
        self._stops: List[str] = []
        self._stop_names: List[str] = []
        for i in complex_string:
            list: List[str] = i.split(' # ')
            self._stops.append(list[0])
            self._stop_names.append(list[1])

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
