# Design / QA Skills

[日本語](README.md)

Two portable skills for coding agents: decide where a software change belongs and what evidence supports its quality.

- [design](skills/design/SKILL.md) inspects the existing system, assigns responsibilities, traces dependencies, and defines observable guarantees.
- [qa](skills/qa/SKILL.md) starts from failure modes and important risks, chooses useful verification, challenges tests, and separates evidence from unknowns.

Each skill works independently. The skills are Markdown and require no runtime, shell, language, framework, or particular agent product.

## Install

Get the public repository:

```sh
git clone https://github.com/MizoTake/design-qa-skills.git
cd design-qa-skills
```

Copy either or both skill folders into the skill directory recognized by your agent. Inspect existing same-name skills before replacing anything.

| Source | Destination layout |
| --- | --- |
| `skills/design/` | `your-skill-directory/design/SKILL.md` |
| `skills/qa/` | `your-skill-directory/qa/SKILL.md` |

Copy the entire individual skill folder. Repository tests and evaluation fixtures are not runtime dependencies. Discovery, automatic selection, and invocation syntax depend on the receiving agent.

### Codex / DeepSeek Harness (DSH) / OpenCode

For a shared installation, copy `design/` and `qa/` into the user-wide `~/.agents/skills/` directory. On Windows, `~` means the user profile directory. Separate copies in each application's skill directory are unnecessary.

```text
~/.agents/skills/design/SKILL.md
~/.agents/skills/qa/SKILL.md
```

| Application | Invocation | Loading verification |
| --- | --- | --- |
| Codex | `$design` / `$qa`, or request the skills in natural language | Installed app-server `skills/list`: both enabled, no discovery errors. |
| DeepSeek Harness (DSH) | "Use the design and qa skills to implement this change." | Installed Skill Registry / filesystem provider: both discovered; bodies match source. |
| OpenCode | "Use the design and qa skills to implement this change." | Running service `opencode api skill.list`: both discovered; bodies match source. |

Verified on Windows on 2026-10-26 with Codex `0.164.0-alpha.11.1`, DSH `0.2.1-rc.3`, and OpenCode `2.1.4`. This verifies discovery and loading, not model execution or measured quality improvement. Installation uses copies: after changing the source, inspect differences and update the installed copies as needed.

Use the skills on the next turn or in a fresh chat. The common Codex directory and `$name` invocation are documented in the [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills).

### skills CLI (optional)

With Node.js / npx available, run this from your working directory and select target agents such as Codex or OpenCode. Cloning first is unnecessary:

```sh
npx skills add MizoTake/design-qa-skills --skill design --skill qa
```

Add `-g` for a user-wide installation. To install only one skill, specify only the corresponding `--skill design` or `--skill qa` option.

```sh
npx skills add MizoTake/design-qa-skills --skill design --skill qa -g
```

For a shared installation including DSH, use the manual method above and place both folders in `~/.agents/skills/`. The skills CLI is optional and may download its own package on first use. CLI installation has not been verified.

## Use

For an agent supporting explicit `$name` invocation:

```text
$design Add caching to the existing search feature. Inspect the existing
responsibilities and cache boundary, and make the smallest coherent change.
```

```text
$qa Fix saved HP=0 loading as 100. Reproduce the reported state and sequence,
then verify the regression and related persistence behavior.
```

```text
Use $design and $qa to implement this API change. Hand the design guarantees
and risks to QA before selecting verification.
```

The same requests work when an environment accepts the skill as prompt context. A review remains read-only unless fixes are authorized. Neither skill grants additional permission.

## Intended difference

| Request | Failure to avoid | Expected behavior |
| --- | --- | --- |
| Add caching | Add storage directly to an arbitrary service | Inspect existing boundaries and responsibility; reuse or justify a boundary. |
| Fix with TDD | Mirror the implementation or test configured mocks | Identify a failure and an independent oracle; confirm the reason for Red. |
| Tests passed | Use the test total as a completion claim | Check relevant regressions and deliverables; disclose verification limits. |

These are intended behaviors, not measured improvement claims.

## Depth and composition

Trivial changes receive an impact check. Small changes receive responsibility analysis and focused verification. Medium and large changes use a design contract, risk analysis, failure modes, and gates. Small changes to high risk contracts still receive deeper scrutiny.

```text
Request -> Design -> Guarantees, invariants, boundaries, risks
                     -> Implementation / QA plan -> Verification -> Evidence
```

The shared handoff fields are `goal`, `contracts`, `invariants`, `boundaries`, `risks`, and `compatibility_requirements`. QA can derive these without a design skill.

Do not generate design documents, test plans, or QA reports for every task. Persist them when requested, required by the project, justified by large changes or handoff, or when documentation is the deliverable. No architecture pattern, coverage target, TDD, or unit testing is universally mandated.

## Validate and evaluate

Repository checks use Python 3.10+ and its standard library, without additional packages:

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -v
```

Checks cover metadata, relative links, independent copying, UTF-8, accidental local absolute paths, paths containing spaces and Japanese, CRLF, and missing optional commands. Metadata validation intentionally accepts this distribution's limited YAML form: `name` plus a single-line JSON-quoted `description`. It is not a general YAML/Markdown parser and does not validate remote URLs or heading anchors.

The [evaluation guide](evals/README.md) includes design and QA scenarios, a deliberately defective persistence fixture, independent contract tests, and a four-condition comparison protocol. The fixture checks establish that the evaluation oracle detects defects and mutations; they do not establish skill effectiveness. Agent comparison results are not yet available.

The [CI matrix](.github/workflows/validate.yml) targets Windows, macOS, and Linux with Python 3.10 and 3.13. A configured matrix is not evidence of successful execution on those platforms.

## v1 scope

The entrypoints remain self-contained, with package checks and initial evaluation cases. Review skills, product-specific plugin adapters, automatic model invocation, and a speculative reference library are outside v1. Add rules through observed failures, a minimal correction, and a corresponding evaluation case.

See the [changelog](CHANGELOG.md). No distribution license has been declared because the owner has not selected one.
