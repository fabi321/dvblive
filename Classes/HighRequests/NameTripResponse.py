from Classes.HighRequests.IDStopNameResponse import IDStopNameResponse
from Classes.HighRequests.IDTripResponse import IDTripResponse
from Classes.Utilities.typings import StopWithoutLineStr


class NameStopResponse(IDTripResponse):
    def __init__(self, start: str, end: str, request_time: int, **kwargs):
        self._start_stop: StopWithoutLineStr = IDStopNameResponse(start).get_stop()
        self._end_stop: StopWithoutLineStr = IDStopNameResponse(end).get_stop()
        IDTripResponse.__init__(self, self._start_stop, self._end_stop, request_time, **kwargs)
