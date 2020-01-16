from Classes.LowRequests.StopNameResponse import StopNameResponse
from Classes.Utilities.request import stop_name_request


class IDStopNameResponse(StopNameResponse):
    def __init__(self, name: str, **kwargs):
        StopNameResponse.__init__(self, stop_name_request(name), **kwargs)
        self.get_stop()
