from typing import List
from Classes.StopWithoutLine import StopWithoutLine

class Line:
    def __init__(self, number: int, string: str, trias_id: str):
        self._number: int = number
        self._string: str = string
        self._trias_id: str = trias_id
        assert type(self._trias_id) == str
        self._stops: [List[StopWithoutLine], None] = None

    def __str__(self) -> str:
        return self._trias_id

    def add_stop(self, stop: StopWithoutLine):
        if not self._stops:
            self._stops = [stop]
        else:
            self._stops.append(stop)

    def get_stops(self) -> List[StopWithoutLine]:
        return self._stops

    def delete_stops(self):
        self._stops.clear()

    def get_line_number(self) -> int:
        return self._number
