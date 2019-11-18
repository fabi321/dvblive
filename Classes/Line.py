from typing import List
#from Classes.Station import StationWithoutLine

class Line:
    def __init__(self, number: int, string: str, trias: str):
        self._number: int = number
        self._string: str = string
        self._trias: str = trias
        self._stops: [List, None] = None

    def __str__(self) -> str:
        return self._trias

    def add_stop(self, stop):
        if not self._stops:
            self._stops = [stop]
        else:
            self._stops.append(stop)

    def get_stops(self) -> List:
        return self._stops

    def delete_stops(self):
        self._stops.clear()

    def get_line_number(self) -> int:
        return self._number
