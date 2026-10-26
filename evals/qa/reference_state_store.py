"""Evaluator-only implementation of the supplied persistence contract."""


class StateStore:
    def __init__(self):
        self._records = {}

    def save(self, user_id, state):
        hp = state.get("hp")
        if type(hp) is not int or not 0 <= hp <= 100:
            raise ValueError("hp must be an integer from 0 through 100")
        self._records[user_id] = dict(state)

    def load(self, user_id):
        return dict(self._records.get(user_id, {"hp": 100}))
