---
name: refactor-safely
description: "Change structure without changing behavior: characterize current behavior, create seams, move in small verified steps, and keep refactors separate from features. Use when cleaning up legacy code, splitting modules, renaming, extracting, replacing a dependency, or paying down technical debt. Prevents big-bang rewrites, silent regressions, and refactor-plus-feature commits that cannot be reviewed or reverted."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: engineering-quality
  standard: agentskills.io
---

# Refactor Safely

Refactoring is a behavior-preserving transformation. If behavior changes, it is a feature or
a bug fix, and it needs its own review. The discipline is simple and often skipped: prove the
current behavior, change one thing, prove it again, and keep the diff reversible.

## When to use

- Code is hard to change, duplicated, misplaced, or coupled.
- A dependency or framework API is being replaced.
- A module is being extracted, split, renamed, or moved.
- A feature needs a seam before it can be added safely.

Do **not** use this as permission for a rewrite. A rewrite is a product decision with a much
larger risk profile; use feature-interrogation and a written decision first.

## Non-negotiables

1. **Behavior stays identical** unless the task explicitly includes a behavior change. If it
   does, split the work: refactor first, behavior second.
2. **Characterize before changing.** If tests do not exist, write them against the current
   behavior — including the weird parts — before touching structure.
3. **Small steps, each verified.** Every step should compile and pass tests. If a step cannot
   be verified in isolation, it is too big.
4. **Keep the public contract stable** until all callers are migrated. Add the new path,
   migrate callers, then remove the old path.
5. **Never mix formatting, moves, renames, and logic** in one commit. Reviewers cannot see
   the real change through the noise.

## Workflow

### 1. Define the target and the invariant

Write two sentences:

```
Target: [structure/quality property we want].
Invariant: [user-visible behavior, API, data, and performance that must not change].
```

If you cannot name the invariant, you are not ready to refactor.

### 2. Map the blast radius

- Who imports/calls this code? Search the whole repo, including tests, scripts, and config.
- Is it a public API, event, route, or database contract used outside the repo?
- What behavior is untested? Those are the dangerous areas.
- What is the rollback unit? A commit, a flag, or a deploy?

### 3. Build a safety net

In order of preference:

1. Existing tests that assert the behavior you are about to move.
2. New characterization tests that pin current outputs for representative inputs.
3. Golden/snapshot tests for serialized output, with a reviewed baseline.
4. Contract tests at the boundary (HTTP, CLI, queue, database).
5. A manual verification script with recorded fixtures, used only when automation is
   genuinely impractical.

Characterization tests are allowed to encode ugly current behavior. Their job is to detect
change, not to endorse the behavior. Mark them clearly so they can be updated when the
behavior is intentionally fixed later.

### 4. Choose a safe pattern

| Situation | Pattern |
| --- | --- |
| Replace an implementation | Branch by abstraction: introduce an interface/seam, swap behind it, remove the old path |
| Migrate callers gradually | Add new API, migrate call sites one by one, delete old API last |
| Split a large module | Extract by dependency direction; move one cohesive responsibility at a time |
| Rename a public symbol | Add alias/deprecated wrapper, migrate, then remove after a release |
| Replace a dependency | Wrap it behind a small adapter, migrate call sites, swap the adapter |
| Untangle shared state | Introduce explicit parameters/return values before moving code |
| Big rewrite temptation | Strangler fig: route a slice through the new path, compare, expand |

### 5. Execute in reversible steps

Each step should have a clear verification:

1. **Prepare:** add the seam/adapter/alias without changing behavior. Tests pass.
2. **Move:** move code with minimal edits (rename detection helps review). Tests pass.
3. **Migrate:** update callers in small batches. Tests pass.
4. **Delete:** remove the old path only when no callers remain. Tests pass.
5. **Clean:** formatting/naming in a separate commit, if at all.

If a step fails, revert that step. Do not "fix forward" through a failing refactor; you lose
the ability to distinguish a structural mistake from a behavior change.

### 6. Verify behavior, not just compilation

- Run the full relevant test suite, not only the touched package.
- Compare outputs for representative fixtures before/after where possible.
- Check performance if the refactor changes data access, allocation, or rendering.
- Check logs/metrics for new errors in a staging run.
- Diff the public API/OpenAPI/schema; it should be empty unless intended.
- Review the diff yourself for accidental changes (default values, error messages,
  ordering, nullability).

### 7. Land and communicate

- Separate commits: preparation, moves, caller migration, deletion, cleanup.
- PR description states the invariant and how it was verified.
- Note any behavior that was intentionally preserved but looks wrong; file it as a follow-up.
- Delete dead code, flags, and compatibility shims after the migration window.

## Scoping rules

- **Rule of three for abstraction.** Extract after the third real duplication, not the
  second imagined one.
- **Moves are not improvements.** Move first, improve later. Reviewers can then see each.
- **No drive-by fixes.** A refactor PR that also fixes a bug cannot be safely reverted.
- **No mass renames without tooling.** Use the language server/IDE rename, then review.
- **No "while I'm here" changes.** They expand blast radius and hide the intended diff.
- **Delete before deprecate.** If nothing uses it and it is not public, remove it.

## Gotchas

- **Tests that assert implementation details** will break during a safe refactor. That is a
  signal the tests are too coupled; fix the tests first, not the design.
- **Mocks can hide behavior changes.** A mock-based test may pass while the real integration
  breaks. Add at least one boundary test.
- **Serialization order matters.** JSON key order, field defaults, and null vs omitted can
  change contracts without changing code logic.
- **Error messages are behavior.** Users and tests may depend on them.
- **Performance can regress silently.** A cleaner abstraction can add a query per item.
- **Feature flags create branches.** A refactor behind a flag needs a plan to remove it.
- **Git history is part of the safety net.** Squashing a multi-step refactor destroys the
  ability to bisect; keep meaningful commits.

## Output contract

```markdown
## Target and invariant
Target: [...]
Must not change: [...]

## Safety net
- Existing tests: [...]
- Added characterization/contract tests: [...]
- Gaps accepted: [...]

## Plan
1. [Step] — verify: [...]
2. [Step] — verify: [...]

## Result
- Commits/steps: [...]
- Behavior verification: [...]
- Public contract diff: [none / explained]
- Performance check: [...]

## Follow-ups
- [Intentional behavior preserved / dead code / flag removal]
```

## Quality gate

- [ ] The invariant is stated and covers user-visible behavior and public contracts.
- [ ] A safety net exists before structural changes; untested areas are called out.
- [ ] Each step is small, reversible, and verified independently.
- [ ] Refactor and behavior change are in separate commits/PRs.
- [ ] No drive-by fixes, mass renames, or formatting noise hide the change.
- [ ] All callers are migrated before the old path is deleted.
- [ ] Performance and serialization/contract behavior were checked.
- [ ] The rollback path is obvious.
