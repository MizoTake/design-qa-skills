"""Run evaluator-only contract assertions against a supplied state_store.py."""

import argparse
import importlib.util
from pathlib import Path
import unittest


def contract_suite(store_type):
    class ContractTests(unittest.TestCase):
        def setUp(self):
            self.store = store_type()

        def save_valid_state(self, user_id, state):
            try:
                self.store.save(user_id, state)
            except ValueError as error:
                self.fail(f"a valid state was rejected: {error}")

        def test_saved_hp_is_preserved(self):
            self.save_valid_state("alice", {"hp": 50})
            self.assertEqual({"hp": 50}, self.store.load("alice"))

        def test_zero_remains_zero(self):
            self.save_valid_state("alice", {"hp": 0})
            self.assertEqual({"hp": 0}, self.store.load("alice"))

        def test_maximum_hp_is_valid(self):
            self.save_valid_state("alice", {"hp": 100})
            self.assertEqual({"hp": 100}, self.store.load("alice"))

        def test_invalid_writes_leave_previous_state_intact(self):
            for hp in (-1, 101, True, False, 1.5, None, "50"):
                with self.subTest(hp=hp):
                    self.save_valid_state("alice", {"hp": 25})
                    with self.assertRaises(ValueError):
                        self.store.save("alice", {"hp": hp})
                    self.assertEqual({"hp": 25}, self.store.load("alice"))

        def test_users_are_isolated(self):
            self.save_valid_state("alice", {"hp": 25})
            self.save_valid_state("bob", {"hp": 75})
            self.assertEqual({"hp": 25}, self.store.load("alice"))
            self.assertEqual({"hp": 75}, self.store.load("bob"))

        def test_unknown_user_receives_default(self):
            self.save_valid_state("alice", {"hp": 50})
            self.assertEqual({"hp": 100}, self.store.load("unknown"))

        def test_save_copies_input(self):
            state = {"hp": 25}
            self.save_valid_state("alice", state)
            state["hp"] = 75
            self.assertEqual({"hp": 25}, self.store.load("alice"))

        def test_load_returns_independent_state(self):
            self.save_valid_state("alice", {"hp": 25})
            state = self.store.load("alice")
            state["hp"] = 75
            self.assertEqual({"hp": 25}, self.store.load("alice"))

    return unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation", type=Path)
    arguments = parser.parse_args()
    specification = importlib.util.spec_from_file_location("candidate_state_store", arguments.implementation)
    if specification is None or specification.loader is None:
        parser.error("implementation must be a readable Python source file")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    result = unittest.TextTestRunner(verbosity=2).run(contract_suite(module.StateStore))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
