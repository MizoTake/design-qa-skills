---
name: qa
description: "Risk-based software QA for coding agents. Use when implementing, fixing, testing, reviewing, or verifying software, including TDD, regression checks, and release readiness. Identify failure modes, choose meaningful verification, challenge important tests, and report executed evidence and unverified risks. Scale down for edits with no behavioral impact."
---

# QA

**Identify the failure a test should detect before writing the test.**
**A useful test failure has a meaningful interpretation as a real defect.**
**Optimize detection of important defects, not test count or coverage.**
**Challenge whether critical tests fail when the implementation is realistically broken.**
**Never report verification that was not performed.**

Use this protocol to detect consequential defects efficiently. Test code is one verification method; compiler, static analysis, integration runs, profiler evidence, visual comparison, and manual reproduction can be better evidence for some risks.

## Scope and authority

Respect the user's task and explicit project rules. A read-only review does not authorize fixes. Do not install dependencies, change live data, publish results, or run destructive fault injection merely because this skill suggests verification. Work within existing authorization and report checks that need a different environment.

Match effort to scope and risk. For a typo or formatting edit with no behavior impact, check the artifact and relevant existing checks without inventing unit tests. For small changes, identify the relevant failure and run focused checks. For medium changes, use an explicit risk/verification plan and the QA gate. For large or high risk changes, include integration, compatibility impacts, staged verification, and any necessary non-functional checks. Do not require every test category for every change.

## 1. Understand the change and existing QA

Read the request, acceptance criteria, diff, relevant implementation and callers, and existing tests. For a bug, preserve the reported input, order, starting state, environment, and expected result. Separate normal behavior from the reported exceptional case.

If a design contract is available, read `goal`, `contracts`, `invariants`, `boundaries`, `risks`, and `compatibility_requirements`. If not, derive the necessary guarantees from the request and inspected behavior. A separate design skill or file is not required. Resolve contradictions between the implementation and the requirement rather than treating the implementation as the source of truth.

Discover the test framework, commands, naming, fixtures, doubles, integration environment, CI, snapshots, static checks, and benchmarks already in use. Inspect whether existing tests detect the relevant failure before adding new ones. Reuse them when sufficient; rewrite or consolidate weak tests within the authorized scope. Avoid introducing a new framework without a demonstrated gap.

## 2. List failures before test cases

State concrete ways the change could fail, and rank them by likelihood and impact, considering how likely existing checks are to miss them. High/medium/low is sufficient; numeric scoring is optional. Prioritize critical behavior and defects with serious user consequences.

For each important failure, connect:

```text
guarantee -> failure mode -> independent oracle -> verification -> evidence
```

For example, a valid zero value being replaced by a default is a failure mode; "test the getter" is not. Include only applicable categories: behavior, boundary, failure, regression, integration, compatibility, and non-functional behavior such as concurrency, security, performance, reliability, or resource use.

Do not invent compatibility requirements. If an API or stored format changes, assess the impact and verify any preservation or migration actually required. Mark unknown requirements as such.

## 3. Choose the least costly adequate verification

Select static checking, unit, component, integration, system/E2E, runtime smoke, visual, benchmark, profiler, log inspection, or manual verification based on the failure. A unit test cannot establish deployment correctness or visual quality on its own. Do not force everything into unit tests or assume broader checks are always better.

Choose expected results from the requirement, a public contract, a known example, an independent calculation, verified prior behavior, an external specification, or an invariant. Do not copy the production algorithm into the test oracle or bless a new snapshot without checking what it represents.

For each important test, explain which real defect its failure would expose. Reconsider tests that only confirm construction, a trivial accessor, a constant, a language/framework feature, or a configured mock. These can be justified by an actual regression or contract; apparent simplicity alone is not grounds for removal.

Prefer observable behavior over private method names, internal call counts, ordering, or structure. An interaction test is useful when the interaction itself is the contract (such as preventing a duplicate payment); document that reason. Do not bind tests to an incidental implementation.

Use mocks for meaningful external, slow, non-deterministic, or difficult-to-trigger boundaries. Consider a fake, in-memory implementation, or real lightweight dependency where it better exercises behavior. Avoid reproducing the implementation as a network of mocks or testing only that a mock returns its configured value.

Set a proportionate test budget: cover distinct important failures without near-duplicate cases. Consolidate overlapping checks and explain any high risk item left uncovered. Coverage can expose gaps but is not a target or proof of quality.

## 4. Implement verification and reproduce regressions

When TDD is requested or required, use:

```text
Intent -> Failure mode -> Red -> Green -> Challenge -> Refactor
```

Confirm that Red fails for the intended behavior when executable; an import, syntax, or setup error is not evidence of reproducing the defect. Make the smallest implementation change for Green and keep checks passing during refactoring. Do not force TDD when a different verification method is more appropriate; explain the choice.

For a bug fix, prefer a regression test that fails on the original bug and passes after the fix using the same reported sequence. If automated reproduction is impractical, use a repeatable manual or runtime procedure. If reproduction fails, state the missing input, environment, or evidence; unrelated passing tests do not establish a fix.

## 5. Execute and challenge

Run the available relevant commands. Start with focused checks, then the related regression/build/integration checks required by the change and project. Broaden or repeat checks when changes, failures, or an unresolved risk justify it. Record command, result, relevant revision/artifact, environment, and useful failure details. Distinguish a failing assertion from collection errors, skipped tests, unavailable commands, and timeouts.

For critical behavior, propose at least one realistic break: change a boundary operator, reverse a condition, return a constant, remove validation, skip a side effect, swallow an exception, or map the wrong field. Identify the assertion expected to catch it. When authorized and practical, execute a mutation in an isolated disposable copy, first confirm the original passes, then verify a behavior assertion fails. A broken import or syntax error does not count as detecting the mutation. Never mutate shared work or live data for this challenge.

An existing mutation tool is optional. A mental challenge is a reasoned expectation only: label it `reasoned, not executed` and do not count it as a detected mutation. A surviving executable mutation indicates a gap, an equivalent change, or an irrelevant expectation to investigate; do not add assertions merely to raise a score.

Check regressions in adjacent callers, error paths, and affected boundaries, not just the edited function. For generated code or distributed artifacts, confirm the fix is present in the actual deliverable. Where a device, service, deployed environment, or performance claim matters, validate there with the same input and conditions. Keep performance quality settings constant or use the agreed quality criterion.

## 6. Apply the QA gate

Before declaring completion, check that:

- The changed guarantees and important failure modes are understood.
- High risk and critical behavior have appropriate verification or explicit gaps.
- Tests have meaningful oracles and are not a collection of implementation mirrors or mock self-tests.
- The reported regression and relevant neighboring behavior were checked.
- Critical tests were challenged, with execution distinguished from reasoning.
- Available required verification ran, and failed/skipped/unavailable checks are identified.
- The evidence refers to the relevant implementation, artifact, and environment.

Use `BLOCK` for an unmet acceptance criterion or a critical unresolved failure. A documented warning or accepted risk must have an explicit basis in the user's authorization and cannot silently turn a failed requirement into success. Continue independent authorized work when an external check is unavailable; report the exact remaining procedure and required user action.

## Output and stopping condition

Report three distinct outcomes, proportionate to the change:

```text
Verified: commands/procedures actually run, results, artifact and environment
Not verified: omitted, unavailable, skipped, or reasoning-only checks, with reasons
Remaining risks: unresolved failure modes and concrete next steps
```

Finish when authorized implementation and relevant executable verification are complete and material limits are explicit. Do not say only "PASS", equate passing tests with overall quality, or hide a required check behind a test total.

Keep the plan in working context by default. Write `TEST_PLAN.md`, `QA_REPORT.md`, or another artifact only if requested, required by the project, useful for a large change or handoff, or itself the deliverable. Capture decisions and evidence rather than private reasoning transcripts. This skill requires no other skill, particular language, framework, tool, or shell.
