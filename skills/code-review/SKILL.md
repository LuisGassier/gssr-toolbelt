---
name: code-review
description: "Review a diff or pull request like a senior engineer: find real defects in correctness, security, concurrency, data, performance, and API contracts, ranked by severity. Use when asked to review code, check a PR, audit a change, or sanity-check an implementation before merge or deploy. Avoids style nitpicking and rubber-stamping; every finding has a location, evidence, impact, and a concrete fix."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: engineering-quality
  standard: agentskills.io
---

# Code Review

Review for the failure that will page someone at 3 a.m., not for the code you would have
written. A good review is a risk assessment with evidence. It is not a style audit and it
is not an approval ritual.

## Non-negotiables

1. **Read the tests and the description before the implementation.** They tell you what the
   author intended and what they verified. Missing tests are a finding, not a footnote.
2. **Review the diff, not the person.** Every comment is about behavior, evidence, and
   impact. No "why did you…", no sarcasm, no rewrite demands.
3. **Rank by severity.** Only P0/P1 block. Everything else is a suggestion or a follow-up.
4. **Cite evidence.** File, line, scenario, and why it matters. "This is wrong" is not a
   review; "this returns 500 when `items` is empty because `[0]` is dereferenced" is.
5. **Do not demand your preferences.** If the linter/formatter does not enforce it and it
   does not affect behavior, it is at most a P3.
6. **Approve when the risk is acceptable.** Waiting for perfection blocks delivery and
   teaches nothing. Request changes when a real defect or missing verification remains.

## Severity model

| Level | Meaning | Action |
| --- | --- | --- |
| **P0** | Data loss, security breach, outage, irreversible corruption | Block. Fix before merge. |
| **P1** | Likely bug, broken contract, missing authz, race, migration hazard | Block or require explicit risk acceptance. |
| **P2** | Real but bounded issue, missing edge case, test gap, performance risk | Should fix; may follow up with owner. |
| **P3** | Readability, naming, local style, optional simplification | Non-blocking suggestion. |

If you cannot explain the user-visible or operational consequence, it is probably not P0/P1.

## Workflow

### 1. Frame the change

- What problem does this solve, and for whom?
- What is the intended behavior change? What must remain identical?
- What is the blast radius: routes, data, permissions, contracts, migrations, money?
- What is the rollback path if this is wrong?
- Is the diff reviewable in one sitting? If > ~400 changed lines or > ~10 files, ask for a
  split or review by risk area. Large diffs hide defects.

### 2. Read the tests

- Do they test behavior or implementation details?
- Do they cover the failure path, not just the happy path?
- Would they fail if the feature broke? A test that cannot fail is worse than no test.
- Are there sleeps, shared state, order dependence, or network calls that make them flaky?
- Is the regression case for the bug actually present?

### 3. Correctness pass

Walk the change as an adversarial user:

- Null, undefined, missing, empty, and zero values.
- Off-by-one and boundary conditions.
- Error paths: thrown, returned, swallowed, logged, retried.
- Async ordering, race conditions, double submits, stale reads.
- State transitions: invalid transitions, partial failure, retries.
- Time: timezone, DST, expiry boundaries, clock skew.
- Numbers: floats for money, integer overflow, rounding, division by zero.
- Encoding: unicode, locale, normalization, truncation.
- Resource cleanup: files, connections, locks, subscriptions, timers.

### 4. Security and privacy pass

- Is authorization checked on **every** path, including direct API calls?
- Is tenant/owner scoping enforced in the query, not just the UI?
- Are inputs parameterized (SQL, shell, templates, paths, URLs)?
- Are secrets out of code, logs, and error messages?
- Is user data logged, cached, or returned more broadly than necessary?
- Are uploads validated by content, size, and destination?
- Are redirects, webhooks, and outbound URLs allowlisted (SSRF)?
- Do new dependencies add known risk or unnecessary surface?

For anything touching auth, money, user data, uploads, or admin actions, read the
`security-review` skill and apply its checklist.

### 5. Data and concurrency pass

- Is the transaction boundary correct? Can a partial write survive an error?
- Are reads and writes consistent under concurrent requests?
- Is the operation idempotent where retries are possible?
- Are migrations backward-compatible with the currently deployed code?
- Are new indexes/constraints safe on a live table?
- Can a retry duplicate a charge, email, job, or row?
- Is cache invalidation correct after the write?

### 6. Performance pass

Only flag what the change plausibly makes worse:

- N+1 queries, unbounded queries, missing indexes on new filters.
- Work inside a loop that could be batched.
- Payload bloat, unnecessary serialization, large responses without pagination.
- Blocking I/O on a hot path or event loop.
- Re-renders, layout thrash, or bundle growth in the browser.
- New synchronous work in a request path that should be async.

Require a measurement for claims of improvement, and a budget for claims of regression.

### 7. Contract and compatibility pass

- Status codes, error shapes, field names, nullability, and defaults.
- Backward compatibility for existing clients and stored data.
- Versioning/deprecation if a public surface changes.
- Feature flags and rollout for risky behavior.
- Observability: can this be debugged in production? Are new failure modes logged/metriced?

### 8. Maintainability pass (P3)

Only after the risk passes:

- Is the logic where a reader will look for it?
- Are names concrete and domain-specific?
- Is there duplicated logic that will drift? (Do not demand premature abstraction.)
- Is the change consistent with nearby patterns?
- Are comments explaining *why*, not *what*?

## Comment format

Use this shape for every non-trivial finding:

```
[P1] src/orders.ts:142 — The total is computed after the discount is applied twice.
Why: a 20% coupon produces a 36% discount and undercharges the customer.
Fix: apply the discount once, or compute `subtotal - discount` from the pre-discount base.
Test: add a case with a percentage coupon and a fixed coupon together.
```

Rules for comments:

- One issue per comment; do not bundle ten concerns into a paragraph.
- State the scenario, not just the rule.
- Suggest a direction, not a full rewrite, unless the fix is small and unambiguous.
- If you are unsure, ask a question instead of asserting a defect.
- Mark optional ideas as `[P3]` or "non-blocking".
- Never comment on generated files, lockfiles, vendored code, or formatting-only changes
  unless they are wrong in a way that matters.

## Review order for large diffs

1. Public contracts and data model (highest blast radius).
2. Auth, permissions, and money paths.
3. Migrations and deployment order.
4. Core logic and error handling.
5. Tests and observability.
6. Naming, structure, and style.

Stop and request a split if you cannot hold the change in your head. A review that misses a
P0 because the diff was 2,000 lines is a process failure, not a reviewer failure.

## What not to do

- Do not approve because CI is green; CI does not test authorization or data loss.
- Do not request changes for personal style preferences.
- Do not rewrite the author's code in a comment. Describe the defect and a direction.
- Do not invent requirements that are not in the description or the product contract.
- Do not block on a P3 while a P1 is unresolved.
- Do not say "LGTM" without stating what you actually checked.
- Do not review only the added lines; deletions and renamed behavior matter.

## Gotchas

- **Moved code looks new.** Use rename detection and review the moved block once.
- **Generated code hides the source.** Review the generator/template, not the output.
- **Formatting noise buries the change.** Ask for a formatting-only commit first.
- **Tests can encode the bug.** A passing test is evidence only if it asserts the right
  behavior.
- **Feature flags can rot.** A flag that is never removed becomes a permanent branch.
- **Config changes are code.** Timeouts, retries, pool sizes, and permissions can cause
  outages even when the diff is one line.
- **Dependency bumps need reading.** A patch bump can change behavior; a major bump needs a
  migration plan.
- **Silent catches are bugs.** `catch {}` turns a failure into corrupt state.

## Output contract

```markdown
## Verdict
[Approve / Approve with follow-ups / Request changes / Needs discussion]

## What I checked
[Diff scope, tests read, areas inspected. Be specific enough to be accountable.]

## Blocking findings
### [P0/P1] [file:line] — [short title]
- Scenario: [...]
- Impact: [...]
- Fix: [...]

## Non-blocking findings
- [P2/P3] [file:line] — [issue and suggestion]

## Test gaps
- [...]

## Questions
- [...]

## Residual risk
[What remains unverified, and what would reduce it.]
```

## Quality gate

- [ ] I read the description, the tests, and the full diff, including deletions.
- [ ] Authorization and tenant scoping were checked on every new path.
- [ ] Error, empty, boundary, and concurrency cases were considered.
- [ ] Data/migration compatibility was checked.
- [ ] Every finding has a location, scenario, impact, and direction.
- [ ] Severity is justified; P3s are clearly non-blocking.
- [ ] I did not demand personal preferences or a rewrite.
- [ ] The verdict matches the findings and states residual risk.
