from Classes.Stop import Stop
from Classes.TripResponse import TripResponse
from request import trip_request, parallel_location


class IDTripResponse(TripResponse):
    def __init__(self, start: Stop, end: Stop, request_time: int, debug: bool = False, line_trias_id: bool = None, **kwargs):
        TripResponse.__init__(self, trip_request(start, end, request_time, True, **kwargs), line_trias_id)
        self._debug: bool = debug
        self._line_trias_id: bool = line_trias_id

    def request_locations(self):
        parallel_location(self._stops, self._debug)