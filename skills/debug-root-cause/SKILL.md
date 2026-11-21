---
name: debug-root-cause
description: "Diagnose a bug to its root cause instead of guessing: reproduce, minimize, observe, test one hypothesis at a time, bisect, fix the cause, and add a regression test. Use when something is broken, flaky, slow, failing in production, or works locally; when an error is unclear; or when previous fixes did not stick. Prevents shotgun debugging, symptom patches, and works-now fixes."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: engineering-quality
  standard: agentskills.io
---

# Debug Root Cause

Debugging is evidence gathering, not code editing. Every change you make before you
understand the failure is a guess that can destroy the evidence. The goal is a causal
statement you can defend: *X happens because Y, which is triggered by Z.*

## Phase 0: Stabilize, then diagnose

If the system is actively harming users, stop the bleeding first:

- Roll back the last deploy, or disable the feature flag.
- Fail over, rate-limit, or shed load.
- Preserve logs, traces, heap dumps, and the failing input before restarting.
- Tell the incident channel what you are doing.

Stabilizing is not fixing. Return to root cause once users are safe. Never let a restart
or a cache flush become the "fix" without an explanation.

## Phase 1: Define the failure

Write down, before touching code:

```
Expected: [what should happen]
Actual:   [what happens instead]
First seen: [time, deploy, version, environment]
Frequency: [always / intermittent / one user / one input]
Impact:   [who is affected, what data or money is at risk]
Repro:    [steps, input, account, device, timing]
```

If you cannot fill this in, your first task is instrumentation, not a fix. "It's broken" is
not a bug report; it is a starting point.

## Phase 2: Reproduce and minimize

A reliable reproduction is the most valuable asset in debugging. It lets you test hypotheses
and prove the fix.

1. Reproduce locally or in a staging environment with the same version, config, and data
   shape as production.
2. Capture the exact input, request, user, timestamps, and feature flags.
3. Reduce it: remove fields, steps, and dependencies until the smallest case still fails.
4. Confirm the reduced case fails consistently. If it is intermittent, quantify the rate
   and find the variable that correlates with failure.
5. Save the reproduction as a failing test if possible. That test becomes your regression
   guard.

If you cannot reproduce, say so and pivot to production observation (traces, logs, metrics,
replays). Do not guess at a fix you cannot verify.

## Phase 3: Observe before theorizing

Read the entire error, not the first line:

- Full stack trace, including `caused by` chains and async boundaries.
- Request ID, user ID, tenant, version, and deployment SHA.
- The exact input and the state at the failure boundary.
- What changed recently: `git log`, deploy history, config changes, data migrations,
  dependency bumps, traffic patterns.

Cheap observation tools, in order:

1. Existing logs, traces, metrics, and dashboards.
2. A debugger or REPL at the failure point.
3. Temporary instrumentation (structured log with the relevant values).
4. Binary search: disable half the system, then half of that.
5. `git bisect` between a known-good and known-bad commit.
6. Replay the failing request or input against a local copy.

Keep a hypothesis log. One line per attempt:

```
H1: cache returns stale user after role change.
  Test: clear cache and repeat; if fixed, H1 supported.
  Result: not fixed — H1 rejected.
```

## Phase 4: Form falsifiable hypotheses

Generate two or three plausible causes, then rank them by likelihood and cost to test.
For each, write the prediction: *if this is the cause, then [specific observation] should be
true*. A hypothesis that cannot be falsified is a story, not a diagnosis.

Use the failure's shape to narrow the search:

| Symptom | Likely classes |
| --- | --- |
| Works locally, fails in prod | Config/env drift, data shape, network, permissions, version |
| Intermittent / under load | Race, pool exhaustion, timeout, retry storm, GC, throttling |
| Wrong value, no error | Stale cache, wrong join, double application, rounding, timezone |
| Fails for some users | Tenant scoping, permissions, locale, data migration, legacy rows |
| Fails after deploy | Backward-incompatible migration, cache key change, contract change |
| Fails on retry / duplicate | Missing idempotency, non-transactional side effects |
| Gradually slower | Unbounded growth, missing index, leak, N+1, log volume |

## Phase 5: Isolate

Change one variable at a time. Use the cheapest discriminating test:

- Toggle the suspect feature flag or config.
- Replace the suspect dependency with a stub.
- Replay the request with one field changed.
- Compare a working account/tenant/row with a failing one.
- Add a boundary log before and after the suspect call.
- Bisect commits, data, or request attributes.

Do not "fix" several things at once. If the symptom disappears, you will not know which
change mattered, and you will have polluted the evidence.

## Phase 6: Fix the cause, not the symptom

A root-cause fix:

- Addresses the mechanism that produced the failure, not just the observed instance.
- Handles the class of input/state, not the one screenshot.
- Considers blast radius: does the fix change behavior for valid cases?
- Does not convert a loud failure into a silent one (`try/catch` that swallows).
- Does not weaken validation, authorization, or tests to make the symptom disappear.
- Includes a regression test that fails before the fix and passes after.

Common non-fixes to reject:

- Increasing a timeout when the real issue is an unbounded query.
- Adding a retry when the operation is not idempotent.
- Clearing a cache on a schedule instead of fixing invalidation.
- Adding a null check at the crash site when the data should never have been null.
- Restarting a process that leaks memory.
- Catching and logging an exception that should propagate.
- Fixing the test to match the buggy behavior.

## Phase 7: Verify and prevent

- Run the regression test and the full relevant suite.
- Re-run the original reproduction, including the production-like data shape.
- Check performance and error rates after the fix.
- Remove temporary logs, debug flags, and instrumentation.
- Document the root cause, the fix, and the detection gap in the PR or incident record.
- Ask: what would have caught this earlier? Add that check if it is cheap.

## Root-cause checklist

Before concluding, rule out the usual suspects:

- Stale cache or CDN; wrong cache key; missing invalidation.
- Async ordering, unawaited promises, shared mutable state, missing locks.
- Timezone/DST, locale, date boundary, clock skew.
- Null vs missing vs empty string; default values applied twice.
- Float arithmetic for money; rounding at the wrong layer.
- Off-by-one, pagination boundaries, inclusive/exclusive ranges.
- Retry without idempotency; duplicate side effects.
- Connection pool exhaustion, leaked handles, unbounded concurrency.
- Config drift between environments; secrets/permissions differences.
- Silent catch, swallowed rejection, ignored error return.
- Data migration that left legacy rows in an invalid state.
- Dependency behavior change after an upgrade.

## Gotchas

- **Heisenbugs.** Instrumentation can hide a race. Prefer low-overhead tracing and
  post-mortem evidence over interactive debugging in production.
- **The error is not the cause.** "Connection reset" may be a downstream timeout, a proxy
  limit, or a crash. Follow the chain to the first abnormal event.
- **Correlation is not causation.** The deploy nearby may be innocent; verify with a
  bisect or a toggle.
- **The failing test may be wrong.** Check the test's assumptions before changing code.
- **Multiple bugs can stack.** Fixing one may reveal the next; re-run the reproduction after
  each change.
- **Production data is part of the system.** A code fix that ignores bad rows is incomplete;
  plan the data repair separately.

## Output contract

```markdown
## Root cause
[One causal sentence: X because Y, triggered by Z.]

## Evidence
- Reproduction: [...]
- Observation that confirmed it: [...]
- Hypotheses rejected: [...]

## Fix
[What changed and why it addresses the cause, not the symptom.]

## Regression test
[Test added, and the behavior it locks in.]

## Verification
[Commands, reproduction, metrics before/after.]

## Prevention
[Detection gap closed, or follow-up with owner.]
```

## Quality gate

- [ ] I can state the root cause in one falsifiable sentence.
- [ ] The failure was reproduced or observed directly, not inferred from a guess.
- [ ] One variable changed at a time; rejected hypotheses are recorded.
- [ ] The fix addresses the mechanism, not just the symptom.
- [ ] A regression test fails without the fix and passes with it.
- [ ] No silent catches, weakened checks, or disabled tests were introduced.
- [ ] Temporary instrumentation was removed.
- [ ] The prevention step is concrete and owned.
