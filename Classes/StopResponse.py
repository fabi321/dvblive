from typing import List
from xml.etree import ElementTree
from elementpath import select
import XPaths
from Classes.Line import Line
from Classes.Response import Response
from Classes.Station import StationWithoutLine


class StopResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], dictionary: bool = False):
        Response.__init__(self, elements, dictionary)
        self._lines: [List[Line], None] = None

    def __get_lines(self):
        self._lines_trias_id: List[str] = select(self._elements, XPaths.line_trias_id, namespaces=self._namespaces)
        self._lines_number: List[str] = select(self._elements, XPaths.line_number, namespaces=self._namespaces)
        self._lines_string: List[str] = select(self._elements, XPaths.line_string, namespaces=self._namespaces)
        self._lines_start: List[str] = select(self._elements, XPaths.line_start, namespaces=self._namespaces)
        self._lines_end: List[str] = select(self._elements, XPaths.line_end, namespaces=self._namespaces)
        self._lines: List[Line] = []
        for i in range(len(self._lines_trias_id)):
            trias_id: str = self._lines_trias_id[i]
            number: int = int(self._lines_number[i])
            string: str = self._lines_string[i]
            line: Line = Line(number, string, trias_id)
            line.add_station(StationWithoutLine(self._lines_start[i]))
            line.add_station(StationWithoutLine(self._lines_end[i]))
            self._lines.append(line)

    def get_lines(self) -> List[Line]:
        if not self._lines:
            self.__get_lines()
        return self._lines