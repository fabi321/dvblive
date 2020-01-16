from Classes.BaseTypes.Line import Line
from Classes.DBManager.Manager import Manager
from Classes.Utilities.typings import LineStr


class DBLine(Manager):
    def __init__(self):
        Manager.__init__(self, 'lines_data', LineStr(''), Line(0, '', LineStr('')))
