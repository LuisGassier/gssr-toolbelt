---
name: acceptance-criteria
description: "Turn a vague feature request into a testable contract: scenarios, edge cases, non-goals, data rules, failure behavior, rollout, and definition of done. Use before implementation when requirements are ambiguous, when writing a ticket or spec, when planning tests, or when two people could disagree about what done means. Produces criteria a developer can build against and a reviewer can verify."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: product-decisions
  standard: agentskills.io
---

# Acceptance Criteria

A requirement is ready when two people can independently decide whether it passed. Until
then, it is a conversation, not a contract. Your job is to expose ambiguity now, when it is
cheap, instead of discovering it during review or after launch.

This skill produces the **contract**, not the implementation plan. It may take ten minutes
or two hours depending on risk; do not turn it into a novel.

## Workflow

### 1. Classify the change

The rigor and shape depend on the type:

| Type | Primary question | Extra sections |
| --- | --- | --- |
| Feature | What new behavior, for whom? | Permissions, empty states, rollout |
| Bug fix | What is wrong, and what is correct? | Reproduction, regression test |
| Refactor | What behavior must remain identical? | Characterization tests, no user-visible change |
| Data/ops | What must be true before, during, after? | Migration, backfill, rollback |
| Integration | What does the external system guarantee? | Timeouts, retries, partial failure |

### 2. Define the job and the boundary

Write the user-visible job in one sentence, then split scope explicitly:

```
In scope:
- [...]
Out of scope (non-goals):
- [...]
```

Non-goals are not decoration. They prevent scope creep and tell the reviewer what not to
expect. If the user did not state them, propose them and ask for confirmation.

### 3. Write scenarios as observable rules

Use Given/When/Then only when it clarifies; otherwise use a rule table. Each criterion must
name an **observable outcome**, not an implementation step.

```
Rule: Invitations expire after 7 days.
Given an invitation created on 1 May at 10:00 UTC
When the invitee opens the link on 8 May at 10:01 UTC
Then the page shows "This invitation has expired" and no account is created.
```

Avoid criteria like "the backend validates the email" — that describes code, not behavior.
Write "an invalid email is rejected with a field-level error and no invitation is sent."

### 4. Cover the edges, not just the happy path

For every input or state transition, decide:

- **Empty** — zero items, blank string, empty list.
- **Missing vs null** — absent field, explicit null, default value.
- **Limits** — min/max length, number range, file size, page size.
- **Unicode and locale** — accents, emoji, RTL, non-Latin names.
- **Time** — timezone, DST, date boundaries, expiry at exactly the boundary.
- **Money** — currency, rounding, negative values, zero, large values.
- **Ordering and duplicates** — stable sort, repeated submits, idempotency.
- **Concurrency** — two users, two tabs, double-click, simultaneous edits.
- **Permissions** — owner, member, admin, outsider, unauthenticated, deleted account.
- **Failure** — dependency down, timeout, rate limit, partial success, retry.
- **Recovery** — refresh, back button, resume, replay, rollback.

You do not need every combination. Choose the ones that would cause real harm or support
cost if wrong, and say why the rest are excluded.

### 5. Specify failure behavior

Happy-path criteria are easy. The contract is incomplete until it says what happens when
things go wrong:

- What does the user see for validation, permission, conflict, and server errors?
- Is the operation retried automatically? Is it safe to retry?
- What is the timeout, and what happens after it?
- Can the operation partially succeed? How is that surfaced?
- Are errors logged with enough context, without leaking secrets or PII?
- Is failure loud (visible) or silent (logged)? Silent success on failure is forbidden.

### 6. Add non-functional criteria when they are material

Only include what this change can realistically violate:

- **Performance:** p95 latency, payload size, query count, render budget.
- **Accessibility:** keyboard path, labels, focus order, announcements, contrast.
- **Security/privacy:** who can read/write, data retention, audit trail, PII in logs.
- **Compatibility:** API clients, old data, browsers, mobile, migrations.
- **Observability:** the event/metric that proves it worked in production.
- **Rollout:** feature flag, cohort, kill switch, rollback procedure.

"It must be secure" is not a criterion. "Only the workspace owner can delete a workspace;
members receive 403; the action is recorded in the audit log" is.

### 7. Close with definition of done

A checklist that a reviewer can run:

- [ ] All acceptance scenarios pass.
- [ ] Edge cases listed above behave as specified.
- [ ] Failure states show the specified message and leave no partial data.
- [ ] Permissions are enforced on the server, not only hidden in the UI.
- [ ] Tests cover the risky scenarios (not every line).
- [ ] Documentation/help text is updated if user behavior changed.
- [ ] Rollout and rollback are defined for risky changes.
- [ ] Open questions are resolved or explicitly deferred with an owner.

## Ambiguity checklist

Scan the request for these and resolve them before writing criteria:

| Ambiguous phrase | Ask instead |
| --- | --- |
| "Users can…" | Which role? Authenticated? Owner? Admin? |
| "Fast" / "instant" | What p50/p95 target, on what device/network? |
| "Secure" | Which threat? Who must be denied? What data is sensitive? |
| "All items" | All matching what filter? Paginated? Sorted how? |
| "Notify them" | Email, in-app, push? On which event? Can it be disabled? |
| "Delete" | Soft delete, hard delete, cascade? Who can restore? |
| "Sync" | Real-time, eventual, on refresh? What wins on conflict? |
| "Default" | Default for new users, existing users, or both? |
| "Etc." | Enumerate the cases or remove the word. |
| "Later" | Is it a non-goal now or an unowned requirement? |

## Worked example: team invitations

```markdown
## Job
A workspace owner can invite a teammate by email with a role, and the invitee can join
once before the invitation expires.

## In scope
- Invite by email; roles: admin, member; expiry 7 days.
- Revoke pending invitation; resend (invalidates the old link).
- Invitee sees workspace name and inviter before accepting.
Out of scope
- Bulk CSV invites, SSO, domain auto-join, custom expiry.

## Rules
1. Given a valid email and role, When the owner invites, Then an invitation is stored with
   a single-use token, the invitee receives one email, and the owner sees it as pending.
2. Given an invitation older than 7 days, When the invitee opens it, Then the page explains
   it expired and no account or membership is created.
3. Given an already-used invitation, When it is opened again, Then it is rejected as used.
4. Given an email that already belongs to a member, When invited, Then the owner sees
   "Already a member" and no duplicate membership is created.
5. Given a non-owner, When they attempt to invite, Then the API returns 403 and no
   invitation is created, even if the UI is bypassed.
6. Given the invitee accepts, Then they become a member with the invited role, the token is
   invalidated, and the owner sees them in the member list.

## Failure behavior
- Email provider failure: invitation remains pending; owner sees "Email not sent — retry".
- Double-click accept: exactly one membership is created (idempotent).
- Expired/revoked token: generic "invalid or expired" message, no email enumeration.
```

## Gotchas

- **Criteria that prescribe implementation** ("use Redis") remove design freedom and age
  badly. Describe behavior and constraints instead.
- **Missing actor.** "The invitation is deleted" — by whom, and can the invitee do it?
- **Boundary off-by-one.** "Expires in 7 days" is ambiguous at exactly 7 days. State the
  comparison and timezone.
- **Tests that mirror the bug.** If the current behavior is wrong, do not encode it as a
  criterion just because a test exists.
- **Acceptance vs tasks.** "Add a database column" is a task, not acceptance. Criteria are
  about observable outcomes.
- **Over-specification.** Do not write 40 scenarios for a copy change. Match rigor to risk
  and reversibility.
- **Unresolved questions hidden in prose.** Put them in an explicit list with an owner and
  a decision date.

## Output contract

```markdown
# [Change name]

## Job
[One sentence.]

## In scope
- [...]

## Out of scope / non-goals
- [...]

## Acceptance rules
1. Given [...] When [...] Then [...]
2. [...]

## Edge cases
- [...]

## Failure behavior
- [...]

## Non-functional requirements
- Performance: [...]
- Accessibility: [...]
- Security/privacy: [...]
- Observability: [...]
- Rollout/rollback: [...]

## Open questions
- [Question] — owner: [...] — needed by: [...]

## Definition of done
- [ ] ...
```

## Quality gate

- [ ] Every criterion has an observable outcome and a clear actor.
- [ ] Non-goals are explicit.
- [ ] The risky edge cases and failure modes are covered.
- [ ] Permissions are specified server-side.
- [ ] Ambiguous adjectives have been replaced with numbers or examples.
- [ ] Open questions are listed, not silently guessed.
- [ ] A developer could build this without asking what "done" means.
- [ ] A reviewer could verify it without reading the implementation.
