from typing import List
#from Classes.Station import StationWithoutLine

class Line:
    def __init__(self, number: int, string: str, trias: str):
        self._number: int = number
        self._string: str = string
        self._trias: str = trias
        self._stations: [List, None] = None

    def __str__(self) -> str:
        return self._trias

    def add_station(self, station):
        if not self._stations:
            self._stations = [station]
        else:
            self._stations.append(station)

    def get_stations(self) -> List:
        return self._stations

    def delete_stations(self):
        self._stations.clear()

    def get_line_number(self) -> int:
        return self._number
