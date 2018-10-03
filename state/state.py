import datetime

class State:

    def __init__(self, user, command):
        self._user = user
        self._cards = []
        self._sets = []
        self._lastCommand = command
        self._timestamp = datetime.datetime.now()

    def getUser(self):
        return self._user

    def setLastCommand(self, str):
        self._lastCommand = str

    def setCards(self, cards):
        self._cards = cards

    def __str__(self):
        return '{};{};{};{};{}'.format(self._user, str(self._cards), str(self._sets), self._lastCommand, str(self._timestamp))