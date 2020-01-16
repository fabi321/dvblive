from typing import List

from Classes.BaseTypes.Time import Time
from Classes.DBManager.Manager import Manager
from Classes.Utilities.typings import TimeStr, SectionStr, JourneyStr, StopWithoutLineStr, ISOTimeStr


class DBTime(Manager):
    def __init__(self):
        Manager.__init__(self, 'times_data', TimeStr(''),
                         Time(StopWithoutLineStr(''), JourneyStr(''), ISOTimeStr('1970-01-01T00:00+00:00'),
                              ISOTimeStr('1970-01-01T00:00+00:00'), SectionStr('')))

    @staticmethod
    def calculate_id(section: SectionStr, journey: JourneyStr) -> TimeStr:
        return TimeStr(section + '=|=' + journey)

    def get_times_for_section(self, section: SectionStr) -> List[TimeStr]:
        section_list: List[str] = section.split('=|=')
        sections: List[TimeStr] = []
        for i in self._mappings.keys():
            if any([h in i.split('=|=') for h in section_list]):
                sections.append(i)
        return sections
