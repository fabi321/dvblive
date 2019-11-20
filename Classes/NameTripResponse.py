from Classes.IDTripResponse import IDTripResponse
from Classes.IDStopNameResponse import IDStopNameResponse
from Classes.Stop import StopWithoutLine

class NameStopResponse(IDTripResponse):
    def __init__(self, start: str, end: str, request_time: int, **kwargs):
        self._start_stop: StopWithoutLine = IDStopNameResponse(start).get_stop()
        self._end_stop: StopWithoutLine = IDStopNameResponse(start).get_stop()
        IDTripResponse.__init__(self, self._start_stop, self._end_stop, request_time, **kwargs)
