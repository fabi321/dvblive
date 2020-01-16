from Classes.LowRequests.StopResponse import StopResponse
from Classes.Utilities.request import stop_request
from Classes.Utilities.typings import StopWithoutLineStr, UnixTime


class IDStopResponse(StopResponse):
    def __init__(self, stop: StopWithoutLineStr, request_time: UnixTime, **kwargs):
        self._debug: bool = kwargs.get('debug')
        StopResponse.__init__(self, stop_request(stop, request_time, 15, return_tree=True, **kwargs))
