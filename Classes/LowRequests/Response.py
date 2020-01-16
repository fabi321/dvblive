from typing import Dict, List
from xml.etree import ElementTree

import ZODB.DB
import ZODB.config

from Classes.Utilities.db_config import zodb_conf


class Response(object):
    _namespaces: Dict[str, str] = {'': "http://www.vdv.de/trias"}
    _db_config: str = zodb_conf

    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        self._elements = elements
        self._dictionary = True if kwargs.get('dictionary') else False
        self._db: ZODB.DB = ZODB.config.databaseFromString(self._db_config)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()
