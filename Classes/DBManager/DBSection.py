from Classes.BaseTypes.Section import Section
from Classes.DBManager.Manager import Manager
from Classes.Utilities.typings import StopStr, SectionStr, LineStr


class DBSection(Manager):
    def __init__(self):
        Manager.__init__(self, 'sections_data', SectionStr(''), Section(StopStr(''), StopStr(''), LineStr('')))

    @staticmethod
    def generate_section_str(start_stop: StopStr, end_stop: StopStr) -> SectionStr:
        return SectionStr(start_stop + '=|=' + end_stop)
