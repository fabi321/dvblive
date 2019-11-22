from typing import List, Dict, Any
from xml.etree import ElementTree
from XPaths import construct_complex_xpath
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
        self._kwargs: Dict[str, Any] = {'tree': self._elements, 'namespaces': self._namespaces}

    def _get_lines(self):
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'line_number', 'line_string', 'line_start', 'line_start_name', 'line_end', 'line_end_name', **self._kwargs)
        self._lines: List[Line] = []
        for i in complex_string:
            list: List[str] = i.split(' # ')
            trias_id: str = list[0]
            number: int = int(list[1])
            string: str = list[2]
            line: Line = Line(number, string, trias_id)
            line.add_stop(StopWithoutLine(list[3], list[4]))
            line.add_stop(StopWithoutLine(list[5], list[6]))
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
        complex_string: str = construct_complex_xpath('StopEvent', False, False, 'stops', 'stop_names', **self._kwargs)[0]
        seperate = complex_string.split(' # ')
        self._stop: StopWithoutLine = StopWithoutLine(*seperate)


    def _get_journeys(self):
        if not self._lines:
            self._get_lines()
        if not self._stop:
            self._get_stop()
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'journey_ref', 'timetable_times', 'estimated_times', **self._kwargs)
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
