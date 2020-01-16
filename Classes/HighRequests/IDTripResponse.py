from Classes.LowRequests.TripResponse import TripResponse
from Classes.Utilities.request import trip_request, parallel_location
from Classes.Utilities.typings import StopWithoutLineStr


class IDTripResponse(TripResponse):
    def __init__(self, start: StopWithoutLineStr, end: StopWithoutLineStr, request_time: int, **kwargs):
        self._debug: bool = kwargs.get('debug')
        self._line_trias_id: bool = kwargs.get('line_trias_id')
        TripResponse.__init__(self, trip_request(start, end, request_time, return_tree=True, **kwargs), **kwargs)

    def request_locations(self):
        parallel_location(self._stops, self._debug)
