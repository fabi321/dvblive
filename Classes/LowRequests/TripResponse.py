import logging
from typing import List, Dict, Any
from xml.etree import ElementTree

from ZODB.Connection import Connection
from transaction import commit

from Classes.BaseTypes.Line import Line
from Classes.BaseTypes.Section import Section
from Classes.BaseTypes.Stop import Stop
from Classes.DBManager.DBLine import DBLine
from Classes.DBManager.DBSection import DBSection
from Classes.DBManager.DBStop import DBStop
from Classes.LowRequests.Response import Response
from Classes.Utilities.XPaths import construct_complex_xpath, complex_xpath_to_dict_list
from Classes.Utilities.typings import Location, StopStr, LineStr, SectionStr

logger: logging.Logger = logging.getLogger('TripResponse')


class TripResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._locations: [List[Location], None] = None
        self._ready_stops: List[StopStr] = []
        self._stops: List[StopStr] = []
        self._line: [LineStr, None] = None
        self._sections: List[SectionStr] = []
        self._predefined_line_trias_id: LineStr = kwargs.get('line_trias_id')
        self._kwargs: Dict[str, Any] = {'tree': self._elements, 'namespaces': self._namespaces}
        if self._predefined_line_trias_id:
            self._kwargs.update({'lineref': self._predefined_line_trias_id})
        commit()

    def _get_cords(self):
        is_lineref = True if self._predefined_line_trias_id else False
        complex_string: List[str] = construct_complex_xpath('Trip', is_lineref, True, 'lats', 'lons', **self._kwargs)
        complex_dict: List[Dict[str, str]] = complex_xpath_to_dict_list(complex_string, 'lats', 'lons',
                                                                        **self._kwargs)
        self._locations: List[Location] = []
        for i in complex_dict:
            self._locations.append({'latitude': float(i['lats']), 'longitude': float(i['lons'])})
        for i in range(len(self._locations) - 1, 1, -1):
            if self._locations.count(self._locations[i]) > 1:
                self._locations.pop(i)

    def get_cords(self) -> List[Location]:
        if len(self._locations) < 1:
            self._get_cords()
        return self._locations

    def _get_line(self):
        is_lineref = True if self._predefined_line_trias_id else False
        complex_string: List[str] = construct_complex_xpath('Trip', is_lineref, True, 'line_number', 'line_string',
                                                            'line_trias_id', **self._kwargs)
        complex_dict: List[Dict[str, str]] = complex_xpath_to_dict_list(complex_string, 'line_number', 'line_string',
                                                                        'line_trias_id', **self._kwargs)
        if len(complex_dict) >= 1:
            line_details: Dict[str, str] = complex_dict[0]
            line_number: int = int(line_details['line_number'])
            line_name: str = line_details['line_string']
            self._line: LineStr = LineStr(line_details['line_trias_id'])
        else:
            logger.warning('Empty TripResponse')
            return
        connection: Connection = self._db.open()
        lines: DBLine = connection.root.lines
        if self._line not in lines.keys():
            lines[self._line] = Line(line_number, line_name, self._line)
        commit()
        connection.close()

    def get_line(self) -> LineStr:
        if not self._line:
            self._get_line()
        return self._line

    def _get_stops(self):
        is_lineref = True if self._predefined_line_trias_id else False
        complex_string: List[str] = construct_complex_xpath('Trip', is_lineref, True, 'stops', 'stop_names',
                                                            **self._kwargs)
        complex_dict: List[Dict[str, str]] = complex_xpath_to_dict_list(complex_string, 'stops', 'stop_names',
                                                                        **self._kwargs)
        self._stops: List[StopStr] = []
        self._stop_names: List[str] = []
        for i in complex_dict:
            self._stops.append(StopStr(i['stops']))
            self._stop_names.append(i['stop_names'])

    def get_stops(self) -> List[StopStr]:
        if len(self._ready_stops) < 1:
            if not self._stops:
                self._get_stops()
            if not self._line:
                self._get_line()
            self._ready_stops: List[StopStr] = []
            connection: Connection = self._db.open()
            stops: DBStop = connection.root.stops
            if self._line:
                for i in range(len(self._stops)):
                    if self._stops[i] not in stops.keys():
                        stops[self._stops[i]] = Stop(self._stops[i], [self._line], self._stop_names[i])
                    elif self._line not in stops[self._stops[i]].get_lines():
                        stops[self._stops[i]].add_line(self._line)
                    self._ready_stops.append(self._stops[i])
            connection.close()
        return self._ready_stops

    def _get_sections(self):
        self._sections: List[SectionStr] = []
        if not self._stops:
            self._get_stops()
        if not self._line:
            self._get_line()
        connection: Connection = self._db.open()
        sections: DBSection = connection.root.sections
        for i in range(1, len(self._stops)):
            section: SectionStr = sections.generate_section_str(self._ready_stops[i - 1], self._ready_stops[i])
            if section not in sections:
                sections[section] = Section(self._ready_stops[i - 1], self._ready_stops[i], self._line)
            if self._line not in sections[section].get_lines:
                sections[section].add_line(self._line)
            self._sections.append(section)
        connection.close()

    def get_sections(self) -> List[SectionStr]:
        if not self._sections:
            self._get_sections()
        return self._sections
