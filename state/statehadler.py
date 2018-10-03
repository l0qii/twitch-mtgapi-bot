from state import State

class StateHandler:

    def __init__(self):
        self._states = []

    # return the current conversation state with a given user if one exists
    def getState(self, user):
        s = [x for x in self._states if x.getUser() == user]
        if len(s) == 0:
            return None
        else:
            return s[0]

    # set the current state of a conversation with a user
    def setState(self, user, command):

        state = None

        if len(self._states) > 0:
            state = [x for x in self._states if x.getUser() == user][0]

        if state is None:
            state = State(user, command)
            self._states.append(state)

    def stateExists(self, user):
        return len([x for x in self._states if x.getUser() == user]) > 0

    def resetState(self, user):
        if self.stateExists(user):
            self._states.remove(self.getState(user))