---
name: pr-craft
description: "Shape changes into reviewable, reversible units: small coherent commits, meaningful messages, PR descriptions with why/how/risk/rollback, self-review, and stacked changes. Use when preparing a PR, cleaning up a messy branch, splitting a large change, writing commit messages, or making a change easy to review and revert. Optimizes for reviewer attention and safe deployment, not for showing every edit at once."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: delivery
  standard: agentskills.io
---

# PR Craft

A pull request is a communication artifact with a deployment risk attached. The reviewer's
 scarcest resource is attention. Your job is to make the change easy to understand, verify,
and revert — not to dump every edit into one branch.

## Non-negotiables

1. **One logical change per PR.** Refactor, feature, dependency bump, and formatting are
   separate PRs.
2. **Small enough to review in one sitting.** Target < ~400 changed lines and < ~10 files;
   split by risk or layer when larger.
3. **Every PR explains why, what, how it was verified, and how to roll back.**
4. **Commits tell a story.** Each commit builds, passes tests, and can be understood alone.
5. **The author self-reviews before requesting review.** Read your own diff first.
6. **No hidden changes.** Generated files, lockfiles, formatting, and renames are called out.

## Workflow

### 1. Define the unit

Write the PR title before writing code:

```
<type>(<scope>): <imperative summary>
```

Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`.
If the title needs "and", it is probably two PRs.

### 2. Start from a clean base

- Rebase or merge the target branch before review; resolve conflicts locally.
- Remove debug logs, commented code, unrelated edits, and local config.
- Run formatter/linter separately; do not mix formatting with logic.
- Check the diff for secrets, credentials, and large binary files.

### 3. Shape commits

Each commit should be a coherent step:

```
feat(invites): add invitation model and expiry
test(invites): cover expiry and duplicate acceptance
feat(invites): expose invite and accept endpoints
docs(invites): document roles and expiry
```

Rules:

- Imperative subject, <= 72 characters, no trailing period.
- Body explains why and any non-obvious trade-off.
- One concern per commit; do not mix a rename with a behavior change.
- Tests belong with the behavior they protect, or in the immediately following commit.
- A commit that cannot pass tests alone is a broken step; squash or reorder it.

For a messy branch:

```bash
git fetch origin
git rebase -i origin/main   # reorder, squash, reword
# or: create a clean branch and cherry-pick coherent chunks
```

Do not rewrite shared history without coordination. Use a new branch when in doubt.

### 4. Split large changes

Split by one of these axes, whichever produces independently reviewable units:

- **Layer:** schema → data access → service → API → UI.
- **Risk:** mechanical rename first, behavior second.
- **Feature slice:** one user-visible path end-to-end, behind a flag.
- **Refactor vs feature:** behavior-preserving prep, then the behavior.
- **Generated vs handwritten:** separate commits/PRs.

Stacked PRs work when each layer depends on the previous. Label the stack, set the base
branch correctly, and do not merge out of order.

### 5. Write the description

```markdown
## Why
[Problem, user impact, link to issue. One paragraph.]

## What
[Behavior change. Not a file list.]

## How verified
- [ ] Unit/integration/e2e commands and results
- [ ] Manual steps with exact inputs
- [ ] Screenshots/video for UI (before/after, real or labeled data)

## Risk
[Blast radius. Auth/data/money/migration/performance. What could break.]

## Rollback
[Flag, revert commit, migration compatibility. What is irreversible?]

## Notes for reviewers
[Where to start, what to ignore (generated), open questions.]
```

Adapt the size: a typo fix needs one line; a migration needs a timeline.

### 6. Self-review

Before requesting review:

- Read the diff top to bottom as if you did not write it.
- Check every `TODO`, `console.log`, commented block, and debug flag.
- Verify the diff contains only intended files.
- Confirm tests actually fail without the change (when practical).
- Re-read the description against the diff; do not claim verification you did not run.
- Check that the title and commits still describe the final change.

### 7. Respond to review

- Treat comments as findings, not attacks. Verify before agreeing or disagreeing.
- Push fixup commits during review; squash before merge if the team prefers.
- Reply with what changed and where, not "done".
- If you disagree, explain the constraint and propose an alternative; do not silently ignore.
- Do not force-push while a reviewer is mid-review unless the team expects it.

### 8. Merge and clean up

- Squash or merge according to the repo convention; do not mix strategies.
- Ensure the final commit message is the one you want in history.
- Delete the branch, close linked issues, update docs/changelog.
- Watch the deploy and the dashboards; a merged PR is not a finished change.
- Revert promptly if it breaks; a clean revert is a feature of a well-shaped PR.

## PR size heuristics

| Size | Review quality |
| --- | --- |
| < 100 lines | High; detailed review likely |
| 100–400 lines | Good; one sitting |
| 400–800 lines | Risky; expect shallow review or requests to split |
| > 800 lines | Split unless generated/mechanical |

Lines are a proxy. A 30-line auth change deserves more scrutiny than a 500-line generated
schema. Split by cognitive load, not just count.

## Gotchas

- **Renames hide changes.** Use `git log --follow` and review the rename separately.
- **Formatting noise buries logic.** A formatter-only commit first makes the real diff small.
- **Lockfiles are not reviewable by eye.** Explain the dependency change in the description.
- **Generated files can drift.** Review the generator and the command, not the output.
- **Feature flags without removal plans** become permanent branches. Add a cleanup task.
- **Stacked PRs rot.** Rebase promptly; keep each layer small and independently green.
- **"Tested manually" is not a test plan.** List the steps and the result.
- **Screenshots without data context** hide empty/error states. Include the edge cases.
- **Squashing destroys the safety net.** For a risky multi-step refactor, keep meaningful
  commits; for a messy WIP branch, squash into a clean story.

## Output contract

When asked to prepare a branch, deliver:

```markdown
## Proposed PR split
1. [Title] — [files/scope] — [why independent]
2. [...]

## Commit plan
- [commit message]
- [commit message]

## PR description
[Why / What / How verified / Risk / Rollback]

## Self-review findings
- [Removed debug code / unrelated edits / missing test]

## Open questions
- [...]
```

When asked to write only the description, deliver the template filled in, with explicit
"not run" markers where verification is missing.

## Quality gate

- [ ] One logical change; title has no "and".
- [ ] Diff is reviewable in one sitting, or split by layer/risk.
- [ ] Commits are coherent, imperative, and independently understandable.
- [ ] Description states why, what, verification, risk, and rollback.
- [ ] No debug code, secrets, unrelated edits, or formatting noise.
- [ ] Self-review completed; claims match what was actually run.
- [ ] Generated/lock/rename changes are called out.
- [ ] Rollback is possible and stated.
