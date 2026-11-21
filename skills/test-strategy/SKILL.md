---
name: test-strategy
description: "Decide what to test, at which level, and what not to test, based on risk rather than coverage theater. Use when adding tests, fixing flaky tests, designing a test suite, choosing unit vs integration vs end-to-end, planning verification for a change, or when asked how much testing is enough. Produces a concrete, prioritized test plan with the failure modes each test protects against."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: engineering-quality
  standard: agentskills.io
---

# Test Strategy

Tests are insurance against specific failures. A suite that does not name the failure it
prevents is just ceremony that slows every change. Design tests from risk: what can break,
how bad is it, and what is the cheapest test that would catch it?

## Core model

```
Risk = impact × likelihood
Test value = (probability of catching a real defect) × (cost of that defect)
             ÷ (maintenance cost + runtime + flakiness)
```

Prioritize tests where a defect is plausible **and** expensive. Do not chase a coverage
number; coverage tells you what executed, not what is verified.

## Workflow

### 1. List the failure modes

For the change or system, write down what can go wrong. Be concrete:

- Wrong result for a valid input.
- Crash on empty/null/missing/large input.
- Authorization bypass or data leak.
- Partial write / duplicate side effect on retry.
- Race under concurrent requests.
- Contract break for an existing client.
- Regression after a dependency or schema change.
- Performance collapse under realistic volume.
- Silent failure that looks like success.

If you cannot name the failure mode, you cannot design the test.

### 2. Choose the cheapest level that catches it

| Failure | Best level | Why |
| --- | --- | --- |
| Pure calculation, parsing, formatting | Unit | Fast, precise, easy to enumerate edges |
| Business rule with a few collaborators | Unit or component | Cheap and readable |
| SQL, transactions, constraints, migrations | Integration against a real database | Mocks hide the actual failure |
| HTTP contract, auth, serialization | Contract/integration | Verifies the boundary clients depend on |
| Critical user journey | End-to-end (few) | High confidence, high cost, brittle |
| Visual layout/regression | Screenshot/visual | Catches what DOM assertions miss |
| Performance budget | Benchmark/load | Only measurement proves it |
| Flaky timing/concurrency | Stress/repeat/property | Sequential tests cannot find races |

Default to the **lowest level that reproduces the real failure**. A unit test with mocked
SQL does not prove a query is correct. An E2E test for a pure function is waste.

### 3. Write the plan before the tests

For each risk, specify:

```
Risk: [failure mode]
Impact: [who/what]
Level: [unit/integration/contract/e2e/visual/load]
Case: [input/state → expected observable outcome]
Why this catches it: [...]
Cost: [runtime/flakiness/maintenance]
```

Prioritize: P0 tests first (data loss, auth, money, core journey), then P1 (likely bugs),
then P2 (edge cases). Explicitly list what you are **not** testing and why.

### 4. Test behavior, not implementation

- Assert observable outputs, state changes, side effects, and errors.
- Avoid asserting private method calls, internal ordering, or exact log strings.
- Use the public API of the unit under test; refactors should not break tests.
- One concept per test, but multiple related assertions are fine if they describe one
  behavior.
- Name tests by the behavior and the condition: `rejects_expired_token_before_creating_user`.
- Make failures explain themselves: include the input and actual vs expected.

### 5. Make tests deterministic

- No real network, clock, randomness, or shared filesystem without control.
- Inject time and IDs; freeze or fake clocks.
- Isolate database state per test (transaction rollback, unique schema, or cleanup).
- Do not use `sleep` to wait for async work; await the actual condition/event.
- Do not depend on test order or shared mutable fixtures.
- Pin dependency versions and seed random generators.
- Run the suite repeatedly and in random order to expose hidden coupling.

### 6. Cover the right edges

Use this checklist, not all of it every time:

- Empty, null, missing, zero, negative, max, overflow.
- Unicode, whitespace, long strings, injection characters.
- Timezones, DST, leap days, expiry boundaries.
- Duplicate submits, retries, idempotency keys, concurrent edits.
- Permission matrix: owner, member, admin, outsider, unauthenticated.
- Dependency failure: timeout, 5xx, malformed response, partial success.
- Migration: old rows, new code, rollback compatibility.
- Error messages and status codes that clients depend on.

Property-based testing is often the cheapest way to cover input space for parsers,
serializers, money math, and state machines. Use it when the invariant is easier to state
than the examples.

### 7. Handle flaky tests as defects

A flaky test is worse than no test because it teaches the team to ignore red.

1. Quarantine it immediately; do not normalize retries.
2. Capture the failure seed, timing, and environment.
3. Find the shared state, race, or uncontrolled dependency.
4. Fix the cause or delete the test if it protects nothing.
5. Re-enable only after it passes repeatedly under stress.

Never "fix" flakiness with a longer sleep or an unconditional retry.

### 8. Define the verification plan for the change

For a PR, state:

- Tests added and the failure each protects against.
- Tests run (unit, integration, e2e, manual) and results.
- Gaps that remain, and the residual risk.
- Any manual verification with exact steps.
- Performance/security checks when relevant.

"Tested manually" without steps is not verification.

## Suite health

- Keep the fast suite fast (< a few minutes locally); push slow tests to CI tiers.
- Run unit tests on every save/commit; integration on every PR; E2E on merge/nightly.
- Track flake rate, runtime, and failures — not just coverage.
- Delete tests that assert dead behavior or duplicate a stronger test.
- Keep fixtures small and readable; a 2,000-line fixture is a maintenance liability.
- Use contract tests at service boundaries instead of duplicating mocks everywhere.

## Anti-patterns

- 100% coverage as a goal; it rewards executing code, not verifying behavior.
- Mocking the thing you are trying to test (the database, the HTTP layer, the framework).
- Asserting on implementation details, private methods, or call counts.
- Snapshot tests with no review of the baseline; they bless regressions.
- One giant integration test that fails without saying why.
- `sleep(1000)` and retries to paper over async races.
- Testing framework behavior instead of your code.
- Writing tests after the implementation to match what it does, without checking what it
  should do.
- Ignoring the test that already caught the bug because "it's flaky".

## Gotchas

- **Test doubles drift.** A mock that no longer matches the real dependency passes while
  production fails. Contract tests catch this.
- **Time and locale are global.** Freeze them explicitly; do not assume the CI machine's
  timezone.
- **Database constraints are behavior.** Test them against the real engine, not an ORM mock.
- **Async tests can pass before the assertion runs.** Always await the assertion or use the
  framework's async guarantees.
- **Coverage can go up while confidence goes down.** New trivial tests can hide a missing
  critical path.
- **E2E tests are a sample, not a proof.** They cover one path; keep the critical few and
  push detail down.

## Output contract

```markdown
## Risks
| Risk | Impact | Level | Test case | Priority |
| --- | --- | --- | --- | --- |

## Tests to add
1. [name] — [behavior] — [why this level]
2. [...]

## Not testing
- [Area] — [why the risk is acceptable or covered elsewhere]

## Verification
- Commands: [...]
- Results: [...]
- Residual risk: [...]
```

## Quality gate

- [ ] Every planned test names the failure it prevents.
- [ ] The level matches the failure; no mocked database for a SQL bug.
- [ ] P0 risks (auth, money, data loss, core journey) are covered first.
- [ ] Tests are deterministic and independent of order/time/network.
- [ ] Assertions check behavior, not implementation details.
- [ ] Flaky tests are treated as defects, not retried away.
- [ ] The plan states what is deliberately not tested.
- [ ] Verification includes commands and results, not just "tests pass".
