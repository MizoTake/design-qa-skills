# Evaluation guide

Package checks establish that the skills can be distributed. Behavioral evaluations establish whether an agent makes useful decisions. Keep these results separate.

## Cases and raw artifacts

- [Design cases](design/cases.md): responsibility placement, local CLI changes, architecture reuse, unjustified abstractions, dependency cycles, legacy code, prototypes, and bug fixes.
- [QA cases](qa/cases.md): low value tests, weak oracles, missing boundaries/regressions, mock-only checks, and failure evidence.
- [Persistence fixture](fixtures/state_store/state_store.py) and its [existing tests](fixtures/state_store/test_state_store.py): deliberately weak tests that pass despite real defects. Copy this entire fixture directory to a disposable workspace for each participant.
- [Fixture contract](fixtures/state_store/CONTRACT.md): requirements supplied to the participant.
- [Four-condition protocol](combined/protocol.md): no skill, design only, QA only, and both skills.

The [oracle](qa/oracle.py) and [correct reference implementation](qa/reference_state_store.py) are evaluator-only artifacts. Do not provide them, the expected findings, or mutation definitions to participants. The reference implementation is a harness check, not the only acceptable design.

## Verify the harness

Run from the repository root with Python 3.10+:

```sh
python -m unittest discover -s evals/fixtures/state_store -v
python evals/qa/oracle.py evals/fixtures/state_store/state_store.py
python evals/qa/oracle.py evals/qa/reference_state_store.py
python -m unittest discover -s tests -v
```

Expected outcomes: the weak existing suite passes; the oracle fails against the defective fixture for zero preservation and invalid writes; the oracle passes against the reference. The last command also checks that realistic mutations fail assertions, rather than only breaking imports. The fixture's failures are intentional and must not be repaired in place.

To evaluate an agent's result, run the same oracle against its copied `state_store.py`, and inspect its generated tests, change set, and evidence. Run participant-generated tests separately against a correct baseline and relevant disposable mutations. Passing this fixed oracle is necessary for this fixture, not sufficient to prove general quality.

## Record results

For each run record skill version or file hash, case ID, model/agent version, environment, input artifact hash, exact request, enabled skills, tool permissions, starting state, and commands/results. Save results outside the skill folders, for example in ignored `evals/results/`. Use the same inputs and resources across conditions; start a fresh context each time to avoid answer leakage.

Measure actual detected defects, assertion-killed non-equivalent mutations, remaining regressions, changed scope, unnecessary abstractions, architecture violations, test maintenance cost, and reviewer findings. Keep test count and coverage as context, not success criteria. Separate observed behavior from reviewer inference. A model judge can assist review, but executable defects and human-checkable contracts provide independent evidence.

These are initial fixtures and a comparison protocol. No baseline-versus-skill agent results are bundled. Improve a rule only after observing a failure, classifying it, making a minimal correction, and adding or updating the corresponding case; then re-run relevant prior cases for regressions.
