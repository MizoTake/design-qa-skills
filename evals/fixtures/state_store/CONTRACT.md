# State store contract

`StateStore.save(user_id, state)` stores a snapshot of a user's state.
`StateStore.load(user_id)` returns a separate snapshot for that user.

- `state` contains an `hp` value that is an integer from 0 through 100 inclusive. Booleans are not valid HP values.
- A valid save followed by load preserves HP, including zero.
- Invalid HP raises `ValueError` before changing previously saved data.
- Users' states do not overwrite each other.
- Loading an unknown user returns `{"hp": 100}`.
- Mutating the input after saving, or the returned snapshot after loading, does not alter saved HP.

Keep the public API. There is no requirement for disk storage, external services, concurrency, additional architecture layers, or a format migration.

Reported reproduction: create a store, save `{"hp": 0}` for user `alice`, then load `alice`. The expected HP is 0; the observed value is 100.
