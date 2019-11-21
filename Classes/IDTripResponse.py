from Classes.StopWithoutLine import StopWithoutLine
from Classes.TripResponse import TripResponse
from request import trip_request, parallel_location


class IDTripResponse(TripResponse):
    def __init__(self, start: StopWithoutLine, end: StopWithoutLine, request_time: int, **kwargs):
        TripResponse.__init__(self, trip_request(start, end, request_time, return_tree=True, **kwargs), **kwargs)
        self._debug: bool = kwargs.get('debug')
        self._line_trias_id: bool = kwargs.get('line_trias_id')

    def request_locations(self):
        parallel_location(self._stops, self._debug)