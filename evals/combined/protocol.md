# Four-condition comparison

Use the same raw fixture, request, resources, permissions, and starting state in four fresh contexts:

1. No added skill.
2. Design only.
3. QA only.
4. Design and QA.

Use this request with a copy of `evals/fixtures/state_store/`:

```text
Fix the reported issue: save {"hp": 0} for one user, then load that user;
the value becomes 100. Keep the public API and satisfy CONTRACT.md.
Inspect the existing implementation and tests, make the necessary repair,
and run appropriate verification. Report evidence and remaining limits.
```

Supply only the copied fixture and enabled SKILL.md files. Keep evaluator material, prior runs, and reference answers out of the context. Do not run a second agent in an already informed session and call it an independent evaluation. Repeat conditions when feasible and record the number of runs and uncertainty; one run cannot establish a causal improvement.

After each run, inspect the diff and evidence, run the independent oracle against the changed file, and challenge participant tests using relevant non-equivalent mutations of a correct baseline. For this fixture, no new abstraction is intrinsically necessary; judge any proposed abstraction by its present boundary or test value, not its name or count alone.

Record a row per condition and run:

| Condition | Contract assertions | Mutations detected / attempted | Regressions | Unnecessary scope / abstractions | Architecture issues | Meaningful tests / reviewed tests | Reviewer findings | Limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use actual command results and human-checkable requirements. Keep mutant syntax/import failures, equivalent mutations, and reasoning-only challenges separate from detected defects. The package's own green tests demonstrate the harness, not the effect of applying the skills. Results are currently unmeasured.
