from state import StateHandler

user = "kevin_spicy"
sh = StateHandler()
sh.setState(user, "card")
print(sh.getState(user))
print(sh.stateExists(user))
sh.resetState(user)
sh.resetState("fdfds")
print(sh.stateExists(user))
