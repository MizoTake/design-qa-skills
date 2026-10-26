class StateStore:
    def __init__(self):
        self._records = {}

    def save(self, user_id, state):
        self._records[user_id] = dict(state)

    def load(self, user_id):
        state = self._records.get(user_id, {})
        return {"hp": state.get("hp") or 100}
