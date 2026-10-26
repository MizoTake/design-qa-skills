from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "evals" / "qa" / "oracle.py"
REFERENCE = ROOT / "evals" / "qa" / "reference_state_store.py"
FIXTURE = ROOT / "evals" / "fixtures" / "state_store"


def run_python(*arguments, cwd=ROOT):
    return subprocess.run(
        [sys.executable, "-I", *map(str, arguments)],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )


class EvaluationHarnessTests(unittest.TestCase):
    def assert_behavior_failure(self, result):
        output = result.stdout + result.stderr
        self.assertEqual(1, result.returncode, output)
        self.assertIn("AssertionError", output)
        self.assertNotIn("ERROR:", output)

    def test_weak_existing_tests_pass_despite_real_defects(self):
        with tempfile.TemporaryDirectory(prefix="qa original ") as temporary:
            workspace = Path(temporary) / "fixture"
            shutil.copytree(FIXTURE, workspace)
            result = run_python("-m", "unittest", "discover", "-s", str(workspace), "-v", cwd=workspace)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Ran 3 tests", result.stderr)

    def test_contract_oracle_detects_reported_zero_and_invalid_write_defects(self):
        result = run_python(ORACLE, FIXTURE / "state_store.py")
        self.assert_behavior_failure(result)
        self.assertIn("FAIL: test_zero_remains_zero", result.stderr)
        self.assertIn("FAIL: test_invalid_writes_leave_previous_state_intact", result.stderr)

    def test_contract_oracle_accepts_correct_reference(self):
        result = run_python(ORACLE, REFERENCE)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Ran 8 tests", result.stderr)

    def test_contract_oracle_detects_realistic_mutations_by_assertion(self):
        source = REFERENCE.read_text(encoding="utf-8")
        mutations = {
            "zero_default": ((
                'return dict(self._records.get(user_id, {"hp": 100}))',
                'return {"hp": self._records.get(user_id, {}).get("hp") or 100}',
            ),),
            "zero_boundary": (("not 0 <= hp <= 100", "not 0 < hp <= 100"),),
            "validation_removed": (("if type(hp) is not int or not 0 <= hp <= 100:", "if False:"),),
            "wrong_user": (
                ("self._records[user_id]", 'self._records["shared"]'),
                ("self._records.get(user_id,", 'self._records.get("shared",'),
            ),
            "constant_return": ((
                'return dict(self._records.get(user_id, {"hp": 100}))',
                'return {"hp": 100}',
            ),),
        }
        with tempfile.TemporaryDirectory(prefix="qa mutations ") as temporary:
            target = Path(temporary) / "state_store.py"
            for name, replacements in mutations.items():
                with self.subTest(mutation=name):
                    mutated = source
                    for original, replacement in replacements:
                        self.assertIn(original, mutated)
                        mutated = mutated.replace(original, replacement)
                    compile(mutated, str(target), "exec")
                    target.write_text(mutated, encoding="utf-8", newline="\n")
                    result = run_python("-B", ORACLE, target)
                    self.assert_behavior_failure(result)


if __name__ == "__main__":
    unittest.main()
