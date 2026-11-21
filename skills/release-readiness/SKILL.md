---
name: release-readiness
description: "Gate a release on evidence: scope, tests, migrations, feature flags, rollback, monitoring, communication, and post-deploy verification. Use before deploying, launching, migrating, or handing off; when preparing a go-live checklist; or when a change is risky, irreversible, or customer-visible. Produces a go/no-go decision with named risks, not a optimistic checklist."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: delivery
  standard: agentskills.io
---

# Release Readiness

Shipping is a risk decision, not a finish line. A release is ready when the team can answer:
what changes, who is affected, how we will know it worked, and how we undo it. If any of those
is missing, the release is not ready — regardless of how green CI is.

## Non-negotiables

1. **Every release has a rollback or a forward-fix plan.** "We'll figure it out" is not a plan.
2. **Schema changes are backward-compatible with the running code** (see migration-safety).
3. **Risky behavior ships behind a flag or a staged rollout.**
4. **Monitoring exists before traffic does.** Know the signal that says it worked.
5. **A named human owns the deploy and the first hour.**
6. **Go/no-go is explicit.** Silence is not approval.

## Workflow

### 1. Classify the release

| Type | Examples | Extra gate |
| --- | --- | --- |
| Code-only | UI, bug fix, internal logic | Tests, rollback |
| Config | Timeouts, limits, flags, secrets | Diff review, restart plan |
| Schema | Column, index, constraint | Expand/contract, migration test |
| Data | Backfill, cleanup, import | Batched, reversible, verified |
| Dependency | Library, runtime, base image | Changelog, audit, canary |
| Infrastructure | Network, IAM, cluster, DNS | Change window, failover |
| Pricing/legal | Money, terms, tax | Owner sign-off, comms |

A release can be several types at once; apply the strictest gate.

### 2. Define the blast radius

- Who is affected: all users, one tenant, one region, internal only?
- What breaks if it fails: read-only, data loss, money, auth, compliance?
- How quickly would we know? What is the detection signal?
- How many users before we can stop? (Canary percentage, flag cohort.)
- Is the change reversible? At what cost, and for how long?

### 3. Pre-flight checks

**Scope and change control**

- [ ] The diff matches the intended change; no unrelated commits.
- [ ] The release is reviewed and approved by the right owner.
- [ ] Feature flags are set correctly for each environment; defaults are safe.
- [ ] The change window avoids peak traffic, blackout dates, and key customers' critical periods.

**Verification**

- [ ] Unit/integration/e2e tests pass on the release commit.
- [ ] Security review completed for auth/data/money/upload changes.
- [ ] Performance checked against the budget for hot paths.
- [ ] Accessibility checked for user-facing UI.
- [ ] Manual smoke test on staging with production-like data.
- [ ] Migration tested on a production-like dump, including old + new code.
- [ ] Rollback tested or explicitly reasoned (flag off / previous image).
- [ ] Backups/snapshots exist for destructive data changes.

**Operations**

- [ ] Dashboards and alerts are live and point at the right service/version.
- [ ] Logs include the new version and a correlation ID.
- [ ] On-call is staffed and knows the release; escalation path is current.
- [ ] Runbook exists for the new failure modes.
- [ ] Capacity/quota can handle the expected traffic.
- [ ] Dependencies and third parties are healthy; no scheduled maintenance.

**Communication**

- [ ] Support/docs know what changed and what to say.
- [ ] Customers are notified for visible/breaking changes.
- [ ] Status page/incident channel is ready if needed.
- [ ] A post-deploy verification owner and time are named.

### 4. Choose a rollout strategy

| Strategy | Use when | Abort signal |
| --- | --- | --- |
| Big bang | Low risk, easily reversible, internal | Error rate/latency spike |
| Canary 1–5% | User-facing, measurable | SLO burn, error spike, support tickets |
| Staged 10→50→100% | Broad impact, need confidence | Same, per stage |
| Feature flag cohort | New behavior, entitlement, beta | Flag-specific metrics |
| Blue/green | Infra/runtime change, fast switch | Health checks, smoke tests |
| Maintenance window | Irreversible migration, downtime accepted | Any failed step |

Define the **abort criteria before starting**: error rate > X%, p95 > Y ms, failed checkout
> Z, data mismatch, or any P0 security signal. If the criteria are met, roll back first and
investigate second.

### 5. Deploy

- Announce start in the release channel with version and scope.
- Deploy in the planned order: schema expand → code → backfill → code switch → cleanup.
- Watch the dashboards during and after each step; do not batch steps to save time.
- Run smoke tests against the real edge, not just the app.
- Record timestamps of each step for later correlation.

### 6. Post-deploy verification

Within the first 15–60 minutes:

- [ ] Error rate and latency at or below baseline.
- [ ] Saturation (CPU, memory, connections, queue) normal.
- [ ] The key business metric moved as expected (orders, signups, jobs).
- [ ] Logs show the new version and no new error class.
- [ ] No spike in support tickets/social reports.
- [ ] Feature flag state matches the plan.
- [ ] Data checks pass (counts, nulls, duplicates, migration state).

If something is wrong: **roll back or flag off first**, preserve evidence, then diagnose.
Do not debug forward on a burning system.

### 7. Close the loop

- Update the changelog/release notes.
- Remove temporary flags and compatibility shims on the planned date.
- Record what was learned; file follow-ups with owners.
- If an incident occurred, write a blameless postmortem with detection and prevention gaps.
- Confirm the rollback window has closed before deleting old data/code.

## Go/no-go template

```markdown
## Release
Version: [...]  Scope: [...]  Owner: [...]  Window: [...]

## Risk
Blast radius: [...]
Reversible: [yes/no — how]
Data impact: [...]

## Evidence
- Tests: [...]
- Security: [...]
- Performance: [...]
- Migration rehearsal: [...]
- Staging smoke: [...]

## Monitoring
Dashboard: [...]  Alerts: [...]  Key metric: [...]
Abort criteria: [...]

## Rollback
[Command/flag/previous version. Time to roll back. What cannot be undone.]

## Decision
GO / NO-GO — [name, time, conditions]
```

## Gotchas

- **Green CI is not release readiness.** It does not test authz, data loss, migrations, or
  production config.
- **The rollback was never tested.** A rollback path that depends on an untested script is a
  hope. Test it on staging.
- **Flags have no owner.** A flag created for a launch becomes a permanent branch. Assign a
  removal date.
- **Migrations and code deploy out of order.** The old code must survive the new schema, and
  the new code must survive the old schema during the window.
- **Config changes bypass review.** A timeout or pool-size change can cause an outage with a
  one-line diff; review it like code.
- **Friday deploys are not the problem; unobserved deploys are.** If nobody is around to
  watch, the timing is wrong regardless of the day.
- **Canary traffic may not represent users.** Internal canaries can miss tenant-specific or
  geo-specific failures. Choose the cohort deliberately.
- **The status page is stale.** Update it before support starts improvising.
- **Irreversible data changes need a backup, not a promise.** Verify the restore path.

## Output contract

Deliver the go/no-go template above, plus:

```markdown
## Blockers
- [ ] [What must be true before GO] — owner: [...] — due: [...]

## Accepted risks
- [Risk] — [why accepted] — [mitigation/monitoring]

## Post-deploy plan
| Time | Check | Owner | Abort if |
| --- | --- | --- | --- |
```

## Quality gate

- [ ] The release type and blast radius are explicit.
- [ ] Tests, security, performance, and accessibility evidence is current.
- [ ] Migration is backward-compatible and rehearsed on realistic data.
- [ ] Rollback/flag-off is tested or concretely reasoned.
- [ ] Monitoring and abort criteria exist before deploy.
- [ ] A named owner is watching the first hour.
- [ ] Support/docs/comms are ready for visible changes.
- [ ] The decision is explicitly GO or NO-GO, with blockers named.
