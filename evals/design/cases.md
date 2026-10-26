# Design cases

Run each prompt in a disposable project with the described raw artifacts. Provide the prompt and raw project only; keep evaluator expectations out of the participant context. Cases without a concrete project yet are scenario specifications, not executed benchmarks.

| ID | Raw project / request | Evaluator checks |
| --- | --- | --- |
| D1 | A large account component handles identity and notifications. A separate report module already exists. Request CSV report export from the account screen. | Reads callers and the report module; places report formatting coherently; avoids adding another unrelated responsibility to the account component or rewriting it wholesale. |
| D2 | A small CLI has one parser and a formatting function. Request a `--quiet` flag. | Inspects exit/output contracts; uses the existing structure; avoids a factory, plugin framework, or mandatory design document. |
| D3 | Features consistently use vertical slices with a shared transaction boundary. Request a new create operation. | Reuses the project's established direction and transaction boundary rather than imposing a different named architecture. |
| D4 | A single pure transformation has no external resources. Request an optional output prefix and suggest making everything extensible. | Distinguishes a present variation from speculative extensibility; selects the smallest useful boundary and explains any abstraction. |
| D5 | Domain types are used by a storage adapter. Request displaying a domain calculation in storage diagnostics. | Traces dependencies; avoids importing the storage adapter into domain code; verifies the actual direction without treating file count as the issue. |
| D6 | A legacy importer loads a documented old file format, and fixtures must remain readable. Request a new optional field. | Reads existing fixtures and explicit compatibility requirements; limits changes and plans regression verification. Does not invent unsupported format promises. |
| D7 | A disposable prototype has no persistence or external users. Request one additional input mode. | Uses proportionate structure; records assumptions without requiring enterprise layers or blocking on routine choices. |
| D8 | The persistence fixture in this repository loads a saved zero as the default. Request fixing that report with minimal changes. | Uses the supplied contract, reproduces the report, identifies the responsible boundary, and avoids an unrelated architectural migration. |

For D8 use `evals/fixtures/state_store/`. For D1-D7, collect a real project or build and version a minimal raw fixture before scoring an agent. Mark those cases `not run` until then. Do not treat a written scenario as a successful behavioral evaluation.
