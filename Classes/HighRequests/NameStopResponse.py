from Classes.HighRequests.IDStopNameResponse import IDStopNameResponse
from Classes.HighRequests.IDStopResponse import IDStopResponse
from Classes.Utilities.typings import StopWithoutLineStr


class NameStopResponse(IDStopResponse):
    def __init__(self, name: str, request_time: int, **kwargs):
        self._stop: StopWithoutLineStr = IDStopNameResponse(name).get_stop()
        IDStopResponse.__init__(self, self._stop, request_time, **kwargs)
