from Classes.BaseTypes.Stop import Stop
from Classes.DBManager.Manager import Manager
from Classes.Utilities.typings import StopStr


class DBStop(Manager):
    def __init__(self):
        Manager.__init__(self, 'stops_data', StopStr(''), Stop(StopStr(''), [], ''))
