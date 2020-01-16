from Classes.BaseTypes.StopWithoutLine import StopWithoutLine
from Classes.DBManager.Manager import Manager
from Classes.Utilities.typings import StopWithoutLineStr


class DBStopWithoutLine(Manager):
    def __init__(self):
        Manager.__init__(self, 'stops_without_line_data', StopWithoutLineStr(''),
                         StopWithoutLine(StopWithoutLineStr(''), ''))
