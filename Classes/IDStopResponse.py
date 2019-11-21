from Classes.StopWithoutLine import StopWithoutLine
from Classes.StopResponse import StopResponse
from request import stop_request


class IDStopResponse(StopResponse):
    def __init__(self, stop: StopWithoutLine, request_time: int,  **kwargs):
        StopResponse.__init__(self, stop_request(stop, request_time, 15, return_tree=True, **kwargs))
        self._debug: bool = kwargs.get('debug')
