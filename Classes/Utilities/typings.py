from typing import NewType, Dict

JourneyStr = NewType('Journey', str)
LineStr = NewType('Line', str)
SectionStr = NewType('Section', str)
StopWithoutLineStr = NewType('StopWithoutLine', str)
StopStr = NewType('Stop', str)
TimeStr = NewType('Time', str)
ISOTimeStr = NewType('ISO Time', str)
UnixTime = NewType('Unix Time', int)
Location = Dict[str, float]
