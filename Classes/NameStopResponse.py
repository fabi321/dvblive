from Classes.IDStopResponse import IDStopResponse
from Classes.IDStopNameResponse import IDStopNameResponse
from Classes.Stop import StopWithoutLine

class NameStopResponse(IDStopResponse):
    def __init__(self, name: str, request_time: int, **kwargs):
        self._stop: StopWithoutLine = IDStopNameResponse(name).get_stop()
        IDStopResponse.__init__(self, self._stop, request_time, **kwargs)
