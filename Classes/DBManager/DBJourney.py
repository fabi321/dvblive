from Classes.BaseTypes.Journey import Journey
from Classes.DBManager.Manager import Manager
from Classes.Utilities.typings import JourneyStr, LineStr


class DBJourney(Manager):
    def __init__(self):
        Manager.__init__(self, 'journeys_data', JourneyStr(''), Journey(LineStr(''), JourneyStr('')))
