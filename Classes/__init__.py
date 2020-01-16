import asyncore
from threading import Thread

import ZEO
import ZODB.Connection
import ZODB.config
import transaction

from Classes.DBManager.DBJourney import DBJourney
from Classes.DBManager.DBLine import DBLine
from Classes.DBManager.DBSection import DBSection
from Classes.DBManager.DBStop import DBStop
from Classes.DBManager.DBStopWithoutLine import DBStopWithoutLine
from Classes.DBManager.DBTime import DBTime
from Classes.Utilities.db_config import zodb_conf, zeo_conf, storage_conf


class ZeoThread(Thread):
    def __init__(self):
        super().__init__()
        self._storage_conf = storage_conf
        self._zeo_conf = zeo_conf

    def run(self) -> None:
        ZEO.server(storage_conf=self._storage_conf, zeo_conf=zeo_conf)
        asyncore.loop()


zeo = ZeoThread()
zeo.start()
db: ZODB.DB = ZODB.config.databaseFromString(zodb_conf)
connection: ZODB.Connection = db.open()
root = connection.root()
try:
    root.stops
except AttributeError:
    root.stops = DBStop()

try:
    root.sections
except AttributeError:
    root.sections = DBSection()

try:
    root.journeys
except AttributeError:
    root.journeys = DBJourney()

try:
    root.lines
except AttributeError:
    root.lines = DBLine()

try:
    root.stops_without_line
except AttributeError:
    root.stops_without_line = DBStopWithoutLine()

try:
    root.times
except AttributeError:
    root.times = DBTime()

transaction.commit()
connection.close()
db.close()
