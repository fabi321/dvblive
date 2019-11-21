from typing import List
from xml.etree import ElementTree
from elementpath import select
import XPaths
from XPaths import construct_simple_xpath, construct_complex_xpath
from Classes.Line import Line
from Classes.Response import Response
from Classes.StopWithoutLine import StopWithoutLine
from Classes.Journey import Journey
from Classes.Time import Time


class StopResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._lines: [List[Line], None] = None
        self._journeys: [List[Journey], None] = None
        self._stop: [StopWithoutLine, None] = None

    def _get_lines(self):
        self._lines_trias_id: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_trias_id), namespaces=self._namespaces)
        self._lines_number: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_number), namespaces=self._namespaces)
        self._lines_string: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_string), namespaces=self._namespaces)
        self._lines_start: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_start), namespaces=self._namespaces)
        self._lines_start_name: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_start_name), namespaces=self._namespaces)
        self._lines_end: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_end), namespaces=self._namespaces)
        self._lines_end_name: List[str] = select(self._elements, construct_simple_xpath(False, False, False, XPaths.line_end_name), namespaces=self._namespaces)
        self._lines: List[Line] = []
        for i in range(len(self._lines_trias_id)):
            trias_id: str = self._lines_trias_id[i]
            number: int = int(self._lines_number[i])
            string: str = self._lines_string[i]
            line: Line = Line(number, string, trias_id)
            line.add_stop(StopWithoutLine(self._lines_start[i], self._lines_start_name[i]))
            line.add_stop(StopWithoutLine(self._lines_end[i], self._lines_end_name[i]))
            self._lines.append(line)

    def get_lines(self) -> List[Line]:
        if not self._lines:
            self._get_lines()
        return self._lines

    def __len__(self) -> int:
        if not self._lines:
            self._get_lines()
        return len(self._lines)

    def _get_stop(self):
        xpath = construct_complex_xpath('StopEvent', False, False, 'stops', 'stop_names')
        complex_string: str = select(self._elements, xpath, namespaces=self._namespaces)[0]
        seperate = complex_string.split(' # ')
        self._stop: StopWithoutLine = StopWithoutLine(*seperate)


    def _get_journeys(self):
        if not self._lines:
            self._get_lines()
        if not self._stop:
            self._get_stop()
        xpath = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'journey_ref', 'timetable_times', 'estimated_times')
        complex_string: List[str] = select(self._elements, xpath, namespaces=self._namespaces)
        for i in complex_string:
            seperate: List[str] = i.split(' # ')
            line: [Line, None] = None
            for i in self._lines:
                if seperate[0] == i:
                    line = i
            if not line:
                raise NotImplementedError('Got different lines from different Xpaths')
            time: Time = Time(self._stop, seperate[2], seperate[3])
            self._journeys.append(Journey(line, seperate[1], times=[time]))

    def get_journeys(self) -> List[Journey]:
        if not self._journeys:
            if not self._lines:
                self._get_lines()
            if not self._stop:
                self._get_stop()
            self._get_journeys()
        return self._journeys
