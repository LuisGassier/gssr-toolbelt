# Trigger catalog (metadata only)

Only the name and description are available to the router, as in a real Agent Skills client.

## acceptance-criteria

Turn a vague feature request into a testable contract: scenarios, edge cases, non-goals, data rules, failure behavior, rollout, and definition of done. Use before implementation when requirements are ambiguous, when writing a ticket or spec, when planning tests, or when two people could disagree about what done means. Produces criteria a developer can build against and a reviewer can verify.

## accessibility-audit

Audit and fix web accessibility to WCAG 2.2 AA: semantics, keyboard access, focus management, labels, contrast, forms, target size, motion, and ARIA restraint. Use when building or reviewing UI, when asked about a11y, accessibility, WCAG, screen readers, or keyboard navigation, or before shipping any user-facing screen. Prioritizes real user blockers over checkbox compliance.

## anti-ai-slop

Detect and remove AI slop from code, UI, copy, docs, tests, and PRs: generic naming, comment noise, over-abstraction, fake data, hedging, emoji headers, purple-gradient sameness, and seamless/robust/leverage filler. Use whenever output feels generic, templated, bloated, or AI-generated, or before shipping anything a human will read. Replaces slop with specific, earned choices instead of swapping one template for another.

## api-contract

Design and evolve APIs that clients can depend on: resource and naming rules, status codes, error shape, idempotency, pagination, filtering, versioning, deprecation, and backward compatibility. Use when adding or changing endpoints, designing a public or partner API, writing OpenAPI, reviewing an API change for breakage, or fixing inconsistent API behavior. Produces a contract, not just a handler.

## clear-writing

Write technical prose that is specific, short, and useful: docs, PR descriptions, commit messages, error messages, UI microcopy, release notes, and incident updates. Use when writing or rewriting any text a human will read, when copy feels vague or corporate, or when an error message needs to tell someone what to do next. Optimizes for the reader's next action, not for sounding impressive.

## code-review

Review a diff or pull request like a senior engineer: find real defects in correctness, security, concurrency, data, performance, and API contracts, ranked by severity. Use when asked to review code, check a PR, audit a change, or sanity-check an implementation before merge or deploy. Avoids style nitpicking and rubber-stamping; every finding has a location, evidence, impact, and a concrete fix.

## debug-root-cause

Diagnose a bug to its root cause instead of guessing: reproduce, minimize, observe, test one hypothesis at a time, bisect, fix the cause, and add a regression test. Use when something is broken, flaky, slow, failing in production, or works locally; when an error is unclear; or when previous fixes did not stick. Prevents shotgun debugging, symptom patches, and works-now fixes.

## dependency-hygiene

Decide whether to add a dependency, keep it healthy, or remove it: build-vs-buy, maintenance signals, security, license, bundle/runtime cost, pinning, update cadence, and unused packages. Use when installing a package, reviewing package.json or requirements, shrinking a bundle or image, responding to an advisory, or cleaning up a stale dependency tree. Treats every dependency as code you now maintain.

## design-system-discipline

Keep UI coherent as it grows: token layers, primitives, variants, composition rules, deprecation, and migration of one-off styles. Use when adding components, reviewing UI consistency, cleaning up arbitrary values, building or extending a design system, or when a product starts to look like five different apps. Optimizes for consistent decisions, not for a component library with every possible prop.

## feature-interrogation

Challenge a feature request before any code is written: test the problem, evidence, user value, alternatives, cost, reversibility, and kill criteria. Use whenever someone asks to build a new feature, add an endpoint, ship an integration, or says can we just add this — especially when the request is vague, solution-shaped, urgent, or expensive. Produces a go/no-go verdict and the smallest valid experiment instead of a task list.

## image-to-ui

Recreate a UI from a screenshot, mockup, or design image with pixel-level fidelity: measure geometry, typography, color, spacing, borders, shadows, assets, and states; build the interface; render and diff against the source; iterate until it matches. Use when asked to copy, clone, reproduce, or match a UI from an image, screenshot-to-code, pixel-perfect implementation, or to make a page look exactly like a design reference. The image is the specification, not inspiration.

## migration-safety

Plan and execute schema and data migrations without downtime or data loss: expand/contract, backward-compatible deploys, batched backfills, lock awareness, verification, and rollback. Use for database changes, column/table renames, backfills, index creation, data cleanup, or any migration that must run on live production data. Treats migrations as multi-deploy operations, not one-way scripts.

## motion-quality

Decide whether and how to animate: purpose, properties, duration, easing, interruption, reduced motion, and performance. Use when adding transitions, micro-interactions, page or route changes, drag and gesture motion, loading states, or when animation feels gratuitous, sluggish, or janky. Produces motion that clarifies cause and effect instead of decorating the interface.

## observability-first

Instrument software so production problems are debuggable: structured logs, metrics, traces, request IDs, SLOs, symptom-based alerts, and runbooks. Use when adding a service, endpoint, job, or integration; when debugging production; or when asked about logging, monitoring, metrics, tracing, alerting, or on-call readiness. Builds observability into the change instead of bolting it on after an incident.

## performance-engineering

Make software faster with measurements, not guesses: define a budget, profile the real hot path, fix the dominant cost (algorithm, I/O, N+1, payload, render), and prove the win with before/after numbers. Use when something is slow, when optimizing a page, API, query, build, or bundle, or when reviewing code for performance risk. Prevents premature optimization, fake wins, and optimizations that only move the cost elsewhere.

## pr-craft

Shape changes into reviewable, reversible units: small coherent commits, meaningful messages, PR descriptions with why/how/risk/rollback, self-review, and stacked changes. Use when preparing a PR, cleaning up a messy branch, splitting a large change, writing commit messages, or making a change easy to review and revert. Optimizes for reviewer attention and safe deployment, not for showing every edit at once.

## refactor-safely

Change structure without changing behavior: characterize current behavior, create seams, move in small verified steps, and keep refactors separate from features. Use when cleaning up legacy code, splitting modules, renaming, extracting, replacing a dependency, or paying down technical debt. Prevents big-bang rewrites, silent regressions, and refactor-plus-feature commits that cannot be reviewed or reverted.

## release-readiness

Gate a release on evidence: scope, tests, migrations, feature flags, rollback, monitoring, communication, and post-deploy verification. Use before deploying, launching, migrating, or handing off; when preparing a go-live checklist; or when a change is risky, irreversible, or customer-visible. Produces a go/no-go decision with named risks, not a optimistic checklist.

## security-review

Threat-model and security-review code, APIs, and data flows: authentication, authorization, tenant isolation, injection, secrets, SSRF, file uploads, sessions, crypto, and dependency risk. Use before shipping anything that touches auth, user data, payments, uploads, admin actions, or the internet; also when auditing an existing app or investigating a suspected vulnerability. Prioritizes exploitable findings over checklist noise.

## simplest-solution

Find the least code, fewest dependencies, and smallest surface area that fully solves the problem. Use when implementing or reviewing a change, when a design feels over-engineered, when asked to reduce complexity, bundle size, or maintenance cost, or when the user asks for the simplest way, less code, no dependencies, or don't over-engineer. Enforces deletion-first and YAGNI without sacrificing correctness, security, or readability.

## test-strategy

Decide what to test, at which level, and what not to test, based on risk rather than coverage theater. Use when adding tests, fixing flaky tests, designing a test suite, choosing unit vs integration vs end-to-end, planning verification for a change, or when asked how much testing is enough. Produces a concrete, prioritized test plan with the failure modes each test protects against.
