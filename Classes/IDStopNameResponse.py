from Classes.StopNameResponse import StopNameResponse
from request import stop_name_request


class IDStopNameResponse(StopNameResponse):
    def __init__(self, name: str):
        StopNameResponse.__init__(self, stop_name_request(name))
        self.get_stop()