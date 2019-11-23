from typing import List, Dict, Any
from xml.etree import ElementTree
from XPaths import construct_complex_xpath
from Classes.Line import Line
from Classes.Response import Response
from Classes.StopWithoutLine import StopWithoutLine
from Classes.Journey import Journey
from Classes.Time import Time
from Classes.MergeableList import MergeableList


class StopResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._lines: [MergeableList, None] = None
        self._journeys: MergeableList = []
        self._stop: [StopWithoutLine, None] = None
        self._kwargs: Dict[str, Any] = {'tree': self._elements, 'namespaces': self._namespaces}

    def _get_lines(self):
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'line_number', 'line_string', 'line_start', 'line_start_name', 'line_end', 'line_end_name', **self._kwargs)
        self._lines: MergeableList = MergeableList([])
        for i in complex_string:
            list: List[str] = i.split(' # ')
            trias_id: str = list[0]
            number: int = int(list[1])
            string: str = list[2]
            line: Line = Line(number, string, trias_id)
            line.add_stop(StopWithoutLine(list[3], list[4]))
            line.add_stop(StopWithoutLine(list[5], list[6]))
            self._lines.append(line)

    def get_lines(self) -> MergeableList:
        if not self._lines:
            self._get_lines()
        return self._lines

    def __len__(self) -> int:
        if not self._lines:
            self._get_lines()
        return len(self._lines)

    def _get_stop(self):
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'stops', 'stop_names', **self._kwargs)
        if len(complex_string) >= 1:
            seperate = complex_string[0].split(' # ')
            self._stop: StopWithoutLine = StopWithoutLine(*seperate)


    def _get_journeys(self, sections: MergeableList):
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'journey_ref', 'timetable_times', 'estimated_times', **self._kwargs)
        for i in complex_string:
            seperate: List[str] = i.split(' # ')
            line: [Line, None] = None
            for i in self._lines:
                if seperate[0] == str(i):
                    line = i
            if line:
                section_trias_id: str = ''
                for j in sections:
                    if str(j).split('=|=')[0] == str(self._stop):
                        section_trias_id = str(j)
                if seperate[3]:
                    time: Time = Time(self._stop, seperate[2], seperate[3], section_trias_id)
                    self._journeys.append(Journey(str(line), seperate[1], times=[time]))

    def get_journeys(self, lines: MergeableList) -> MergeableList:
        if not self._journeys:
            if not self._lines:
                self._get_lines()
            if not self._stop:
                self._get_stop()
            self._get_journeys(lines)
        return self._journeys
