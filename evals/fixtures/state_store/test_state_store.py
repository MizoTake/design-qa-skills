import unittest

from state_store import StateStore


class ExistingTests(unittest.TestCase):
    def test_store_can_be_constructed(self):
        self.assertIsInstance(StateStore(), StateStore)

    def test_records_start_empty(self):
        self.assertEqual({}, StateStore()._records)

    def test_records_object_is_stable(self):
        store = StateStore()
        self.assertIs(store._records, store._records)


if __name__ == "__main__":
    unittest.main()
