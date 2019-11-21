from typing import Dict, List
from xml.etree import ElementTree


class Response(object):
    _namespaces: Dict[str, str] = {'': "http://www.vdv.de/trias"}

    def __init__(self, elements: List[ElementTree.ElementTree], **kwargs):
        self._elements = elements
        self._dictionary = True if kwargs.get('dictionary') else False
