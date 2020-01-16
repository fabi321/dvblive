from typing import List, Dict, Any
from xml.etree import ElementTree

from ZODB.Connection import Connection

from Classes.BaseTypes.Journey import Journey
from Classes.BaseTypes.Line import Line
from Classes.BaseTypes.StopWithoutLine import StopWithoutLine
from Classes.BaseTypes.Time import Time
from Classes.DBManager.DBJourney import DBJourney
from Classes.DBManager.DBLine import DBLine
from Classes.DBManager.DBSection import DBSection
from Classes.DBManager.DBStopWithoutLine import DBStopWithoutLine
from Classes.DBManager.DBTime import DBTime
from Classes.LowRequests.Response import Response
from Classes.Utilities.XPaths import construct_complex_xpath, complex_xpath_to_dict_list
from Classes.Utilities.typings import StopWithoutLineStr, LineStr, JourneyStr, SectionStr, TimeStr, ISOTimeStr


class StopResponse(Response):
    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        Response.__init__(self, elements, **kwargs)
        self._lines: List[LineStr] = []
        self._journeys: List[JourneyStr] = []
        self._stop: [StopWithoutLineStr, None] = None
        self._kwargs: Dict[str, Any] = {'tree': self._elements, 'namespaces': self._namespaces}

    def _get_lines(self):
        connection: Connection = self._db.open()
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'line_number',
                                                            'line_string', 'line_start', 'line_start_name', 'line_end',
                                                            'line_end_name', **self._kwargs)
        lines: DBLine = connection.root().lines
        stops: DBStopWithoutLine = connection.root().stops_without_line
        self._lines: List[LineStr] = []
        for i in complex_string:
            list: List[str] = i.split(' # ')
            trias_id: LineStr = LineStr(list[0])
            if not trias_id in lines.keys():
                number: int = int(list[1])
                string: str = list[2]
                line: Line = Line(number, string, trias_id)
                lines[trias_id] = line
            if lines[trias_id].get_len_stops() < 2:
                lines[trias_id].delete_stops()
                start_stop: StopWithoutLineStr = StopWithoutLineStr(list[3])
                lines[trias_id].add_stop(start_stop)
                if start_stop not in stops.keys():
                    stops[start_stop] = StopWithoutLine(start_stop, list[4])
                end_stop: StopWithoutLineStr = StopWithoutLineStr(list[5])
                lines[trias_id].add_stop(end_stop)
                if end_stop not in stops.keys():
                    stops[end_stop] = StopWithoutLine(end_stop, list[6])
            self._lines.append(trias_id)
        connection.close()

    def get_lines(self) -> List[LineStr]:
        if len(self._lines) == 0:
            self._get_lines()
        return self._lines

    def __len__(self) -> int:
        if len(self._lines) == 0:
            self._get_lines()
        return len(self._lines)

    def _get_stop(self):
        connection: Connection = self._db.open()
        stops: DBStopWithoutLine = connection.root().stops_without_line
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'stops', 'stop_names',
                                                            **self._kwargs)
        if len(complex_string) >= 1:
            separate = complex_string[0].split(' # ')
            trias_id: StopWithoutLineStr = StopWithoutLineStr(separate[0])
            name: str = separate[1]
            if trias_id not in stops.keys():
                stops[trias_id] = StopWithoutLine(trias_id, name)
            self._stop: StopWithoutLineStr = stops[trias_id]
        connection.close()

    def _get_journeys(self, sections: List[SectionStr]):
        connection: Connection = self._db.open()
        db_sections: DBSection = connection.root().sections
        journeys: DBJourney = connection.root().journeys
        times: DBTime = connection.root().times
        complex_string: List[str] = construct_complex_xpath('StopEvent', False, False, 'line_trias_id', 'journey_ref',
                                                            'timetable_times', 'estimated_times', **self._kwargs)
        complex_dict: List[Dict[str, str]] = complex_xpath_to_dict_list(complex_string, 'line_trias_id',
                                                                        'journey_ref', 'timetable_times',
                                                                        'estimated_times', **self._kwargs)
        for i in complex_dict:
            line: [LineStr, None] = None
            for j in self._lines:
                if i['line_trias_id'] == j:
                    line = j
                    break
            if line:
                section_trias_id: SectionStr = SectionStr('')
                for j in sections:
                    if j.split('=|=')[0] == str(self._stop):
                        section_trias_id = j
                if section_trias_id != '':
                    journey: JourneyStr = JourneyStr(i['journey_ref'])
                    time: TimeStr = TimeStr(times.calculate_id(section_trias_id, journey))
                    if i['estimated_times'] and time not in times.keys():
                        if journey not in journeys.keys():
                            journeys[journey] = Journey(line, journey)
                            self._journeys.append(journey)
                        timetable_time: ISOTimeStr = ISOTimeStr(i['timetable_times'])
                        estimate_time: ISOTimeStr = ISOTimeStr(i['estimated_times'])
                        times[time] = Time(self._stop, journey, estimate_time, timetable_time, section_trias_id)

    def get_journeys(self, sections: List[SectionStr]) -> List[JourneyStr]:
        if not self._journeys:
            if not self._lines:
                self._get_lines()
            if not self._stop:
                self._get_stop()
            self._get_journeys(sections)
        return self._journeys
