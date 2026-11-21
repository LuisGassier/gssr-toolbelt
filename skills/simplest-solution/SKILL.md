---
name: simplest-solution
description: "Find the least code, fewest dependencies, and smallest surface area that fully solves the problem. Use when implementing or reviewing a change, when a design feels over-engineered, when asked to reduce complexity, bundle size, or maintenance cost, or when the user asks for the simplest way, less code, no dependencies, or don't over-engineer. Enforces deletion-first and YAGNI without sacrificing correctness, security, or readability."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: engineering-craft
  standard: agentskills.io
---

# Simplest Solution

The best code is code that does not exist. After that, it is code the platform already
provides, then code with one obvious implementation, then code with an abstraction.

Minimal does **not** mean terse, clever, or untyped. It means the smallest change that is
correct, secure, readable, and maintainable for the actual requirement. Code golf is a
different sport and it loses.

## Non-negotiables

1. **Solve the stated problem only.** No speculative options, hooks, plugin points, or
   "future-proofing" unless the user named the future use case.
2. **Delete before adding.** Remove dead code, duplicate helpers, unused dependencies, and
   redundant config before writing anything new.
3. **Platform before package.** Use the language, framework, database, or browser feature
   that already exists before adding a dependency.
4. **One implementation before an abstraction.** Duplicate twice; abstract on the third
   real use. A wrong abstraction is more expensive than duplication.
5. **Data and constraints before application code.** A database constraint, type, or CSS
   rule is usually smaller and safer than runtime validation or JavaScript.
6. **Never trade correctness for line count.** Do not drop validation, error handling,
   accessibility, authorization, or tests to make a diff look small.

## Workflow

### 1. Pin the outcome

Write one sentence: the observable behavior that must be true when this is done. List the
hard constraints: compatibility, latency, security, data volume, existing APIs. If the
outcome is fuzzy, use the acceptance-criteria skill first; do not invent scope.

### 2. Inventory what already exists

Search before writing:

- Is the behavior already implemented behind a flag or in another module?
- Is there an existing helper, component, endpoint, or query that can be reused?
- Does the framework already solve this (routing, validation, caching, i18n, dates)?
- Does the database already enforce it (unique, foreign key, check, default)?
- Is there a dependency already installed that does it (check before adding another)?

Report what you found. "I added a new helper" is a red flag when an existing one existed.

### 3. Choose the cheapest sufficient mechanism

Prefer mechanisms in this order, unless the domain says otherwise:

| Need | Cheapest sufficient option |
| --- | --- |
| Static content | Markup or a constant, not a CMS or database |
| One value that varies by environment | Config/env var, not a settings system |
| Validation | Type system, schema, or DB constraint, not hand-written branching |
| Derived state | Compute it, do not cache or store it |
| One query | Direct SQL/ORM call, not a repository layer |
| Two call sites | A function, not an interface + factory + registry |
| Layout and states | CSS and platform behavior, not a JS state machine |
| Date/number formatting | `Intl`, not a library |
| HTTP | Platform `fetch`, not an HTTP client wrapper |
| Background work | A cron/job primitive, not a queue and worker service |
| Search | Database full-text/`LIKE` for small data, not a search cluster |

### 4. Set a complexity budget

Before implementing, state the budget. Defaults:

- New dependencies: **0** unless the alternative is materially worse. Justify each one.
- New public APIs or exports: **0** unless required by a caller.
- New abstractions (interface, base class, generic, registry): **0** until three real uses.
- New configuration knobs: **0** until two real consumers or a deployment need.
- New services, queues, caches, or datastores: **0** unless measurement proves the need.
- Files touched: as few as possible, but do not hide logic in a god file.

A budget is not a hard limit; it is a forcing function. If you exceed it, say why.

### 5. Implement the smallest honest diff

- Put logic where a reader will look for it.
- Keep names concrete and domain-specific.
- Handle the failure modes the requirement actually has.
- Add the smallest test that would fail if the behavior broke.
- Do not mix refactoring with behavior change; use refactor-safely when cleanup is needed.

### 6. Validate

Run the project's existing checks (format, lint, typecheck, tests, build). Then answer:

- What did I delete or avoid building?
- What complexity did I add, and why is it earned?
- What would break if this code disappeared?
- Is there a smaller version that still passes the acceptance criteria?

## Decision rules

- **YAGNI beats "we might need it."** Add the second use case when it exists.
- **Rule of three beats DRY.** Two similar blocks are cheaper than one misleading abstraction.
- **Boring beats novel.** Choose the tool the team can debug at 3 a.m.
- **Data over code.** Move invariants into schemas and constraints.
- **Constraints over validation.** Make invalid states unrepresentable.
- **Composition over configuration.** Small pieces beat a framework with 20 flags.
- **Deletion over deprecation** when nothing uses the code; deprecate only when callers exist.

## Anti-patterns to remove on sight

- `utils.ts` / `helpers.py` dumping grounds with unrelated functions.
- An interface with exactly one implementation and no test double.
- A repository/service/controller layer for a single CRUD table.
- A state library for one form or one boolean.
- A caching layer with no measured latency problem and no invalidation plan.
- An event bus for two in-process callers.
- A plugin system for zero third-party plugins.
- A microservice for a module that shares a database and a deploy.
- An ORM for one query; raw SQL for 40 complex queries. Match the tool to the work.
- Custom date, currency, slug, or UUID code when the platform has it.
- A new dependency for one function that is five lines of standard library.
- Premature pagination, multi-tenancy, or internationalization with one tenant and one locale.

## Gotchas

- **"Simple" can move complexity to operations.** A hand-rolled queue is fewer lines but
  more on-call risk than a managed job runner. Count operational complexity too.
- **Deleting code can break consumers.** Check imports, routes, events, and external
  clients before removing a public surface.
- **Framework magic is not free.** A one-line framework feature can hide a query, a
  re-render, or a security default. Know what it does.
- **Small diffs can hide big decisions.** A column type change is small in lines and large
  in consequences; treat it as a design change.
- **Do not simplify away observability.** Removing logs or metrics to shrink a diff makes
  production debugging harder, not simpler.
- **Readability is a feature.** If the minimal version requires a comment to explain the
  trick, it is probably not minimal.

## Output contract

For an implementation, report:

```markdown
## Outcome
[One sentence: what now works.]

## Smallest change
[What was added/changed/deleted, and where.]

## Complexity budget
- New dependencies: [n] — [why]
- New public APIs: [n] — [why]
- New abstractions: [n] — [why]
- New config: [n] — [why]

## Deliberately not built
- [Speculative feature/abstraction] — [why it is not needed yet]

## Validation
[Commands run and results. Tests added.]
```

For a review, list each simplification with location, current cost, smaller alternative,
and risk of the change.

## Quality gate

- [ ] The change solves the stated outcome, not a guessed future one.
- [ ] Existing code, framework features, and platform APIs were checked first.
- [ ] New dependencies and abstractions are zero or explicitly justified.
- [ ] Nothing was deleted that external callers still use.
- [ ] Correctness, security, accessibility, and tests were not traded for brevity.
- [ ] The diff is the smallest one that a maintainer can understand.
- [ ] A second, smaller option was considered and rejected for a stated reason.
