---
name: design
description: "Software change design for coding agents. Use for features, bug fixes, refactoring, API or data changes, or design consultation when responsibilities, dependencies, interfaces, or change boundaries require judgment. Inspect the existing system and choose the smallest coherent change. Skip the full protocol for edits without a design decision."
---

# Design

**Understand the existing system before designing a replacement or extension.**
**Justify abstractions with a present responsibility, boundary, variation, or dependency.**
**Before adding behavior, identify the component's current and proposed responsibilities.**
**Prefer the smallest coherent change that respects the project's architecture.**

Use this protocol to decide where a change belongs and what it must guarantee. It works for functions, modules, components, packages, services, and systems; it does not prescribe an architecture pattern.

## Scope and authority

Follow the user's task and explicit project instructions, including architecture decisions and contribution rules. This skill does not authorize unrelated refactors, dependency installation, external writes, or destructive operations. A design consultation remains a consultation unless implementation was requested.

Use the full protocol for a meaningful design decision, including a small edit that changes a public contract, persistence, authentication, billing, security, or concurrency. For typo, comment, wording, formatting, or a plainly local constant edit with no behavioral contract impact, only check the impact. An explicit request to use this skill still receives proportionate treatment.

Calibrate depth using both scope and risk:

| Depth | Work |
| --- | --- |
| Trivial | Check for contract impact; make the requested edit. |
| Small | Read the affected code and callers, check responsibility, choose verification. |
| Medium | Form a design contract, assess risks and change radius, use both gates below. |
| Large | Compare viable options, analyze architecture and compatibility risks, plan staged changes and verification. |

A high risk one-line change needs more scrutiny than a large mechanical edit. Classify the change as feature, bugfix, refactor, migration, performance, security, compatibility, maintenance, or prototype only to choose useful work; do not turn classification into a deliverable.

## 1. Inspect before proposing

Read the relevant instructions, repository structure, affected implementation, callers and dependencies, analogous features, existing tests, configuration, build/format/lint commands, CI, and documentation. Search for an existing solution before adding a mechanism. Record the relevant file or symbol as evidence for architectural claims; distinguish inspected facts from assumptions.

Read only as far as needed to understand the change and its important consequences. Missing access is a limit to report, not evidence that an implementation or rule does not exist. For a new project, derive a minimal structure from the actual requirements.

## 2. Extract the requirement

Identify the goal, required behavior, constraints, non-goals, explicit compatibility requirements, and unknowns. Separate required changes from useful adjacent work and unrelated improvements. Include adjacent work only when it is necessary for the requested result, and explain why.

Use an explicit assumption for an unknown that does not materially affect correctness or the chosen boundary. Ask a focused question when plausible interpretations would materially change the outcome. Continue independent work while a blocking answer is pending. Do not invent compatibility layers or migration promises; assess the impact and honor the requirements actually given.

## 3. Locate responsibility and dependencies

For each affected component, compare its current responsibility with the proposed behavior. Explain why they belong together. If they change for different reasons, inspect an appropriate existing component or consider composition or a small new boundary. Do not use this rule to split every function into another component.

Before introducing an interface, factory, repository, service layer, event bus, generic framework, or extension point, identify the present need: real variation, an existing boundary, required dependency inversion, or a useful test seam. A hypothetical future implementation is insufficient. A single implementation may still have a real boundary; count is not the deciding factor.

Trace dependency direction, including cycles, hidden dependencies, unnecessary global state, service locator use, and reaching across module boundaries. Judge against this project's architecture. Layered, vertical slice, ECS, data-oriented, plugin, and other designs can all be valid; pattern names alone do not justify a change.

## 4. Form the design contract

For medium or large work, keep a concise decision record in working context. For large changes, compare reasonable options and their tradeoffs before choosing. Capture observable guarantees rather than implementation instructions alone:

```text
goal: requested outcome
affected_components: existing and proposed locations
responsibilities: current responsibility -> proposed responsibility, with rationale
contracts: inputs, outputs, failures, and observable side effects
interfaces: any public surface that changes
data_flow: entry -> processing -> storage or output
dependencies: direction and new boundaries, if any
invariants: guarantees that must remain true
boundaries: module, runtime, data, and external-system seams
compatibility_requirements: explicitly required behavior; otherwise impact and unknowns
non_goals: excluded work
risks: important ways the change could fail
assumptions: unresolved facts being used
```

Assess direct edits and transitive impact on callers, public APIs, stored data, tests, deployment artifacts, and runtime behavior. Ask whether one requirement is spreading across responsibilities unnecessarily; file count is not a quality metric. When useful, simulate one or two plausible changes (a dependency change or another input kind) to expose rigidity. Do not build speculative extension points to satisfy the simulation.

The portable handoff to QA consists of `goal`, `contracts`, `invariants`, `boundaries`, `risks`, and `compatibility_requirements`. A separate QA skill is optional; these fields also support direct verification.

## 5. Apply the design gate

Before implementing medium or large changes, check that:

- The goal and non-goals are understood and supported by the request.
- Relevant existing implementations and their responsibilities were inspected.
- The placement of new behavior and dependency direction can be explained.
- Each new abstraction has a current justification.
- Public contract and data impacts have been assessed.
- Important guarantees have observable verification boundaries.

Resolve gaps as `BLOCK`, `WARNING`, or `ACCEPTED RISK`, with the affected guarantee and next action. Block dependent work when a missing fact prevents a correct or authorized implementation. A warning can permit independent work. An accepted risk needs a stated basis within the user's authorization; the label cannot grant permission or hide an unmet requirement. Do not require user approval for routine implementation choices merely to satisfy a gate.

## 6. Implement and compare

When implementation is requested, make the necessary change using existing conventions and tools. Coordinate ownership before touching shared changes. Keep required work separate from unrelated findings.

Compare the resulting implementation with the contract: responsibility drift, unexpected dependencies, global state, duplicated knowledge, and expanded change radius. Revise the design when evidence warrants it and record the material reason. Execute available checks appropriate to the guarantees; a design explanation alone is not verification. Hand the contract to QA when available.

## Output and stopping condition

Finish when the requested design or implementation is delivered, significant design gaps are resolved or explicitly bounded, and evidence and remaining limits are reported. Summarize the change, its placement and rationale, the checks actually run, and unresolved risks. Do not claim runtime or architecture validation that was not performed.

Keep the contract in working context by default. Create a design document only when requested, required by the project, justified by a large change, needed for a handoff, or itself the deliverable. Save decisions and evidence, not private reasoning transcripts. Do not require `DESIGN.md`, a second skill, a particular tool, or a particular framework to use this skill.
