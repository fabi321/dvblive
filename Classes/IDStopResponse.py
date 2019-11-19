from Classes.Stop import Stop
from Classes.StopResponse import StopResponse
from request import stop_request


class IDStopResponse(StopResponse):
    def __init__(self, stop: Stop, request_time: int, debug: bool = False, **kwargs):
        StopResponse.__init__(self, stop_request(stop, request_time, 15, True, debug=debug, **kwargs))
        self._debug: bool = debug