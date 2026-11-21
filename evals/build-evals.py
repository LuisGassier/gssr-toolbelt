#!/usr/bin/env python3
"""Build skills/<name>/evals/evals.json from the catalog below.

The fixture is shared: evals/fixtures/legacy-app. Each eval names a task and objective
assertions. Run this script after editing the catalog.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = "evals/fixtures/legacy-app"

EVALS = {
    "feature-interrogation": {
        "name": "vague-ai-recommendations",
        "prompt": (
            "We need to add AI-powered recommendations to the dashboard for the Q4 launch. "
            "The request is in docs/FEATURE-REQUEST.md. Decide whether we should build it "
            "and what the smallest next step is. Do not write production code."
        ),
        "expected_output": (
            "A verdict that challenges the request, identifies missing evidence, considers "
            "alternatives including doing nothing, prices maintenance/security, and proposes "
            "a cheap experiment with kill criteria."
        ),
        "assertions": [
            "Does not start implementing the recommendation engine",
            "Separates the stated solution from the underlying user problem",
            "Explicitly assesses evidence and flags what is missing",
            "Considers at least three alternatives including doing nothing",
            "Gives one explicit verdict (BUILD, BUILD SMALL, LEARN FIRST, NOT NOW, or NO)",
            "Defines a small experiment or kill criteria with a decision rule",
        ],
    },
    "simplest-solution": {
        "name": "minimal-currency-and-cache",
        "prompt": (
            "Implement a helper that formats currency for the dashboard and a per-request "
            "cache for user lookups. Use the existing code in src/lib/utils.js. Keep the "
            "change as small as possible."
        ),
        "expected_output": (
            "Minimal implementation using Intl.NumberFormat, no new dependencies, reuses or "
            "removes existing helpers, rejects a speculative cache, and states a complexity "
            "budget."
        ),
        "assertions": [
            "Uses Intl.NumberFormat or platform formatting instead of adding a dependency",
            "Does not add a caching layer without a measured need, or explicitly rejects it",
            "Deletes or avoids speculative abstractions and unused helpers",
            "States a complexity budget covering dependencies, abstractions, and config",
            "Keeps the diff small and readable",
        ],
    },
    "acceptance-criteria": {
        "name": "team-invitations-contract",
        "prompt": (
            "Turn this into acceptance criteria before implementation: add team invitations "
            "with roles (admin/member) and a 7-day expiry, including revoke and resend. Use "
            "the repo for context but focus on invitations."
        ),
        "expected_output": (
            "Testable rules, edge cases, failure behavior, permissions, non-goals, open "
            "questions, and a definition of done."
        ),
        "assertions": [
            "Writes observable Given/When/Then or rule-based criteria",
            "Covers expiry boundary, used/revoked token, duplicate member, and non-owner authorization",
            "States explicit non-goals",
            "Covers failure behavior such as email failure, double accept, and invalid token",
            "Includes a definition of done and open questions",
            "Avoids prescribing implementation details such as Redis or specific tables",
        ],
    },
    "code-review": {
        "name": "pre-ship-server-review",
        "prompt": (
            "Review server.js before we ship it. Focus on defects that would block release. "
            "Give file/line evidence and concrete fixes."
        ),
        "expected_output": (
            "Finds SQL injection, missing authorization on admin delete, PII/password logging, "
            "N+1 queries, blocking I/O, swallowed errors, and weak secret/JWT handling, ranked "
            "by severity."
        ),
        "assertions": [
            "Flags SQL injection in /api/users",
            "Flags missing authorization on the admin delete endpoint",
            "Flags PII or password logging in /api/login",
            "Flags the N+1 query pattern in /api/orders",
            "Flags blocking readFileSync and/or swallowed errors",
            "Ranks findings by severity and gives file/line plus a fix",
        ],
    },
    "debug-root-cause": {
        "name": "cart-concurrency-bug",
        "prompt": (
            "The cart total is sometimes wrong when two users add items at the same time. "
            "Find and fix the root cause. Add a regression test."
        ),
        "expected_output": (
            "Identifies shared module-level mutable state, explains the concurrent-request "
            "scenario, scopes state per request/session, and adds a regression test."
        ),
        "assertions": [
            "Identifies the shared mutable module-level total as the root cause",
            "Explains the concurrent-request scenario that produces the wrong total",
            "Fixes by scoping state per request or session, not by hiding the symptom",
            "Adds a regression test that exercises concurrency",
            "Does not merely add a try/catch, sleep, or restart",
        ],
    },
    "refactor-safely": {
        "name": "utils-behavior-preserving-cleanup",
        "prompt": (
            "Clean up src/lib/utils.js without changing behavior. It is used across the app. "
            "Keep the refactor reviewable."
        ),
        "expected_output": (
            "States the behavior invariant, characterizes current behavior, moves in small "
            "steps, preserves or explicitly migrates exports, and keeps refactor separate "
            "from behavior change."
        ),
        "assertions": [
            "States the behavior invariant explicitly",
            "Adds or identifies characterization tests before structural change",
            "Preserves or explicitly migrates the public exports",
            "Does not change behavior such as date/currency output or fallbacks",
            "Keeps changes small and reversible",
        ],
    },
    "test-strategy": {
        "name": "risk-based-test-plan",
        "prompt": (
            "We have almost no meaningful tests. What should we test first, and at what "
            "level? Use the existing server and tests as the starting point."
        ),
        "expected_output": (
            "A risk-based plan prioritizing authorization and data integrity, using integration "
            "tests against a real database for SQL/transactions, including cart concurrency "
            "and contract tests, and explicitly deprioritizing low-risk areas."
        ),
        "assertions": [
            "Prioritizes authorization and data-integrity risks first",
            "Recommends integration tests against a real database for SQL/transaction behavior",
            "Includes a concurrency test for cart state",
            "Names specific failure modes rather than generic coverage",
            "Explicitly says what not to test or deprioritize",
            "Avoids treating 100% coverage as the goal",
        ],
    },
    "security-review": {
        "name": "pre-internet-security-audit",
        "prompt": (
            "Audit this app before exposing it to the internet. Report exploitable issues and "
            "release blockers with concrete fixes."
        ),
        "expected_output": (
            "Finds SQL injection, missing authorization, hardcoded/committed secrets, PII "
            "logging, weak JWT/dependency risk, and ranks severity with fixes."
        ),
        "assertions": [
            "Finds SQL injection in /api/users",
            "Finds missing authorization on the admin delete endpoint",
            "Finds the hardcoded JWT secret and/or committed secrets in .env.example",
            "Finds PII or password logging",
            "Flags weak/outdated JWT handling or dependency risk",
            "Ranks severity and gives concrete fixes and verification",
        ],
    },
    "performance-engineering": {
        "name": "orders-api-performance",
        "prompt": (
            "The orders API and dashboard feel slow. Make them faster, but show your "
            "measurements and reasoning. Do not guess."
        ),
        "expected_output": (
            "Defines a budget, requires a baseline, identifies the N+1 loop and SELECT *, "
            "recommends batching/joins, indexes, pagination, and proves the win before/after."
        ),
        "assertions": [
            "Requires a baseline measurement before optimizing",
            "Identifies the N+1 query loop in /api/orders",
            "Recommends batching/join and selecting only needed columns",
            "Considers pagination, indexes, and payload size",
            "Does not add caching as the first fix without measurement",
            "Proposes before/after verification with realistic data",
        ],
    },
    "migration-safety": {
        "name": "live-orders-status-migration",
        "prompt": (
            "We need to add a NOT NULL status column to orders and an index, on a live "
            "production table. Review and rewrite db/migrations/001_add_status.sql safely."
        ),
        "expected_output": (
            "Expand/contract plan, lock timeouts, concurrent index, validated constraint, "
            "batched backfill, verification, and rollback/cleanup."
        ),
        "assertions": [
            "Rejects running the migration as one blocking step",
            "Uses lock_timeout/statement_timeout or equivalent guardrails",
            "Uses CREATE INDEX CONCURRENTLY for the live table",
            "Adds the column/constraint in a backward-compatible expand phase",
            "Batches the backfill instead of one large UPDATE",
            "Includes verification and rollback/cleanup",
        ],
    },
    "api-contract": {
        "name": "partner-orders-api-contract",
        "prompt": (
            "Review openapi.yaml and the orders endpoints for an external partner API. Fix "
            "the contract and list breaking changes."
        ),
        "expected_output": (
            "Consistent error shape/status codes, cursor pagination, idempotency for POST, "
            "documented authz, versioning/deprecation, and a list of breaking changes."
        ),
        "assertions": [
            "Flags errors returned with HTTP 200 and inconsistent error shapes",
            "Requires one consistent error schema and correct status codes",
            "Adds idempotency for order creation and retries",
            "Replaces or bounds offset pagination with cursor pagination",
            "Documents authentication/authorization and versioning",
            "Identifies breaking changes for existing clients",
        ],
    },
    "anti-ai-slop": {
        "name": "remove-slop-from-readable-surfaces",
        "prompt": (
            "Quita el AI slop del README, del Dashboard y del formulario de registro. "
            "Quiero que se sienta específico y humano, no como una plantilla generada."
        ),
        "expected_output": (
            "Responds in Spanish, identifies fake proof and visual clichés, removes or flags "
            "placeholders, replaces vague copy with specifics, and does not invent proof."
        ),
        "assertions": [
            "Responds in Spanish",
            "Identifies fake proof or unsupported metrics such as trusted by thousands, 99.9%, or 10x",
            "Identifies generic visual clichés such as purple/indigo gradients, glassmorphism, and three equal cards",
            "Removes or flags placeholder testimonials such as John Doe and Acme",
            "Replaces vague copy with specific text or explicitly asks for missing facts",
            "Does not invent new metrics or testimonials",
        ],
    },
    "clear-writing": {
        "name": "readme-and-error-rewrite",
        "prompt": (
            "Rewrite the README and the API error messages so a new developer can actually "
            "run the app and fix failures."
        ),
        "expected_output": (
            "Leads with what the app is and who it is for, adds runnable prerequisites and "
            "configuration, removes fake claims, and rewrites errors with cause and next action."
        ),
        "assertions": [
            "Leads with what the app is and who it is for",
            "Adds runnable prerequisites, setup steps, and configuration",
            "Removes or flags fake claims and testimonials",
            "Rewrites errors to say what happened, why, and what to do",
            "Keeps the text concise and specific",
        ],
    },
    "pr-craft": {
        "name": "split-messy-working-tree",
        "prompt": (
            "This working tree has a mix of feature, refactor, formatting, and debug changes. "
            "Prepare it for review: propose commits and a PR description. Do not change "
            "behavior beyond organizing the change."
        ),
        "expected_output": (
            "Splits commits by concern, separates refactor/formatting from feature, writes "
            "imperative messages, includes why/how verified/risk/rollback, and removes debug code."
        ),
        "assertions": [
            "Proposes splitting the change into coherent commits by concern",
            "Separates refactor/formatting from feature behavior",
            "Writes imperative commit messages",
            "PR description includes why, how verified, risk, and rollback",
            "Calls out and removes debug code or formatting noise",
            "Does not mix unrelated changes in one commit",
        ],
    },
    "accessibility-audit": {
        "name": "signup-form-wcag-22-aa",
        "prompt": (
            "Audit src/components/SignupForm.jsx for accessibility and fix the blockers. "
            "We target WCAG 2.2 AA."
        ),
        "expected_output": (
            "Real form/button semantics, persistent labels, keyboard/focus and error handling, "
            "contrast/target-size/motion fixes, minimal ARIA, proportional changes."
        ),
        "assertions": [
            "Replaces the clickable div with a real button or form submit",
            "Adds persistent visible labels associated with each input",
            "Addresses keyboard/focus and error announcement or association",
            "Flags contrast, target size, or motion issues such as animate-pulse and the tiny submit",
            "Avoids ARIA that substitutes for native semantics",
            "Keeps the fix proportional and does not redesign the whole app",
        ],
    },
    "design-system-discipline": {
        "name": "minimal-token-system-migration",
        "prompt": (
            "The dashboard uses one-off colors, radii, shadows, and buttons. Establish a "
            "minimal design system and migrate the touched components without redesigning "
            "the product."
        ),
        "expected_output": (
            "Token layers, semantic names, primitives/variants, full states, migration plan, "
            "and no unused variants or large component library."
        ),
        "assertions": [
            "Defines token layers (primitive/semantic/component) rather than a flat list",
            "Replaces raw hex or arbitrary values in the touched components",
            "Consolidates inconsistent buttons into variants with states",
            "Includes focus, disabled, error, and loading states",
            "Provides a migration path and avoids adding unused variants",
            "Does not redesign the product or add a large component library",
        ],
    },
    "motion-quality": {
        "name": "purposeful-dashboard-motion",
        "prompt": (
            "Add motion to the dashboard and signup flow so it feels alive, without making it "
            "slow or distracting."
        ),
        "expected_output": (
            "Purpose gate, small token set of durations/easings, transform/opacity only, "
            "reduced-motion support, and removal of gratuitous pulse/hover-scale effects."
        ),
        "assertions": [
            "Questions whether each animation has a purpose before adding it",
            "Removes or replaces gratuitous animate-pulse and hover-scale effects",
            "Specifies durations, easings, and compositor-friendly properties",
            "Honors prefers-reduced-motion",
            "Avoids animating layout properties or blocking input",
            "Keeps motion consistent with a small token set",
        ],
    },
    "observability-first": {
        "name": "on-call-debuggability",
        "prompt": (
            "Make this service debuggable in production. Add the logging, metrics, tracing, "
            "and alerts you would need on call."
        ),
        "expected_output": (
            "Structured logs with request/trace IDs, no PII, RED/USE metrics, business events, "
            "trace propagation, SLO/alerts, and a runbook plus verification."
        ),
        "assertions": [
            "Replaces console.log with structured logs including request/trace IDs",
            "Removes or redacts PII and passwords from logs",
            "Adds RED/USE metrics and key business events",
            "Adds trace propagation across HTTP/DB and async work",
            "Defines symptom-based alerts/SLO with a runbook",
            "Includes a verification plan such as a synthetic failure",
        ],
    },
    "release-readiness": {
        "name": "friday-signup-and-migration-go-no-go",
        "prompt": (
            "We are deploying the new signup flow and the orders status migration on Friday. "
            "Give a go/no-go with blockers. Be explicit about risk and rollback."
        ),
        "expected_output": (
            "Release classification, blast radius, migration compatibility/rehearsal, flags, "
            "rollback, monitoring, comms, post-deploy checks, and an explicit go/no-go."
        ),
        "assertions": [
            "Classifies the release types and blast radius",
            "Blocks or conditions the release on migration compatibility and rehearsal",
            "Requires a rollback or flag-off plan and monitoring",
            "Names post-deploy verification and abort criteria",
            "Covers communication/support and a named owner",
            "Gives an explicit GO/NO-GO with blockers, not vague optimism",
        ],
    },
    "dependency-hygiene": {
        "name": "package-json-audit",
        "prompt": (
            "Audit package.json. Decide what to remove, replace, or keep, and flag supply-chain "
            "risk. Give a concrete plan with verification."
        ),
        "expected_output": (
            "Identifies unused lodash/moment/request/left-pad, deprecated or risky packages, "
            "platform replacements, lockfile/install-script/license checks, and a removal plan."
        ),
        "assertions": [
            "Identifies unused dependencies such as lodash, moment, request, and left-pad",
            "Flags deprecated or risky packages such as request, moment, and old jsonwebtoken",
            "Recommends platform replacements such as fetch and Intl where appropriate",
            "Checks the transitive tree, install scripts, lockfile, and license",
            "Does not add new dependencies without justification",
            "Gives a concrete removal/update plan with verification",
        ],
    },
    "image-to-ui": {
        "name": "pixel-level-dashboard-reproduction",
        "fixture": "evals/fixtures/ui-reference",
        "prompt": (
            "Reproduce the UI in reference.png exactly at 1440x900 CSS px and DPR 1. Match the "
            "layout, typography, palette, spacing, borders, icons, and every visible detail. "
            "Build index.html and styles.css, render it, diff it against the reference with the "
            "image-to-ui probe, and iterate until the remaining differences are explained."
        ),
        "expected_output": (
            "A faithful static reproduction with measured tokens, a same-viewport render, a "
            "numeric diff, and an honest list of inferred behavior and remaining deviations."
        ),
        "assertions": [
            "Identifies the 1440x900 CSS viewport and DPR 1",
            "Reproduces the 232px sidebar plus main shell with measured geometry",
            "Matches the display serif and UI sans typography with measured sizes and weights",
            "Samples the paper, forest, accent, and border colors instead of guessing",
            "Reproduces the sidebar nav, stat cards, observations table with status pills, and right rail",
            "Renders at 1440x900 and provides a diff image with a numeric mismatch",
            "States inferred responsive/states behavior and any remaining deviations",
        ],
    },
}


def main() -> None:
    for skill, spec in EVALS.items():
        evals_dir = ROOT / "skills" / skill / "evals"
        evals_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "skill_name": skill,
            "evals": [
                {
                    "id": 0,
                    "name": spec["name"],
                    "prompt": spec["prompt"],
                    "expected_output": spec["expected_output"],
                    "files": [spec.get("fixture", FIXTURE)],
                    "assertions": spec["assertions"],
                }
            ],
        }
        path = evals_dir / "evals.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
