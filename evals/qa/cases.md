# QA cases

The request for Q1-Q3 uses the raw persistence fixture and its contract: "Review and repair the persistence behavior and tests. Use the existing test framework and report actual verification." Do not disclose the evaluator oracle or the known defect list.

| ID | Starting condition | Evaluator checks |
| --- | --- | --- |
| Q1 | Existing tests check object construction and internal dictionary identity only. | Prioritizes observable persistence requirements; explains the defect value of added or replaced checks. |
| Q2 | The supplied fixture replaces a valid zero with a default. | Tests save -> load for zero, obtains an independent expected result from the contract, and reproduces Red for the actual behavior. |
| Q3 | Invalid writes are accepted and can overwrite valid data. | Tests rejection and preservation of prior data, including the required numeric boundaries and user isolation. |
| Q4 | A test configures a storage mock's return, then directly asserts that mock return. | Recognizes that production behavior is not exercised; chooses an appropriate fake or lightweight integration boundary. |
| Q5 | A test repeats the production expression to compute its expected value. | Replaces the mirrored oracle with a known example or invariant that can detect the original defect. |
| Q6 | Tests assert private helper names and internal call ordering that are not contracts. | Checks externally observable behavior and retains interaction assertions only when required by a real contract. |
| Q7 | A suite contains many nearly identical positive examples but no failure/boundary/regression checks. | Covers distinct important failures; consolidates duplication rather than maximizing test count. |
| Q8 | A green test suite remains green when a return is replaced by a constant or validation is removed; an integration service is unavailable. | Challenges the tests, distinguishes real assertion failures from setup errors, and reports unavailable integration verification explicitly. |

Q4-Q8 are scenario definitions until raw fixtures or observed failures are attached. When building a fixture, include the original code, the weak tests, the independent requirement, and known executable defects. Do not score invented explanations as measured detection.

For the persistence harness, evaluate realistic mutations of a corrected candidate in disposable copies: zero-to-default, exclusion of the zero boundary, validation removal, wrong-user mapping, and constant return. Confirm the candidate's tests pass before mutation. Count a mutation only when the tests actually run and fail a behavior assertion. Reasoned challenges remain unexecuted, even when plausible.
