from xml.etree import ElementTree
from elementpath import select
from typing import List
import XPaths

tree = ElementTree.parse("Stop-Response-DorotheaErxleben.xml")
test: List[ElementTree.Element] = select(tree, XPaths.stoerung, namespaces={'': "http://www.vdv.de/trias"})
for i in test:
    print(i.text)