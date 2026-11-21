# Evaluation results — November 2026

## Method

- **21 skills**, each with `SKILL.md`, optional `references/`, scripts, and `evals/evals.json`.
- **21 behavioral runs**, one per skill, against a shared fixture (`evals/fixtures/legacy-app`) or
  the UI reference fixture (`evals/fixtures/ui-reference`), each in an isolated `evals/runs/<skill>/repo`.
- **123 assertions** in total, graded against each run's `outputs/report.md` and the files it changed.
- **Trigger test:** 42 realistic queries — 21 positives (one per skill) and 21 near-misses. The router
  saw only `name + description`, as in a real Agent Skills client.
- **Static validation:** `python3 scripts/validate-skills.py` → 0 errors.
- **Scripts:** `scan_slop.py`, `scan_a11y.py`, `perf_gate.py`, and `image_probe.py` were run against
  fixtures, including expected failures and exact-match/diff cases.
- **Constraints:** fixture runs were offline; no `npm install`, network, or external services. This is
  stated in every report. Results are static/local evidence, not a production deployment.

## Summary

| Metric | Result |
| --- | --- |
| Behavioral assertions | **123 / 123 passed** |
| Positive triggers | **21 / 21** |
| Near-miss non-triggers | **21 / 21** |
| Overall trigger accuracy | **42 / 42 (100%)** |
| Static validation errors | **0** |
| Skills | **21** |

The first trigger pass scored **41/42**; the one "miss" was a mislabeled negative (a flaky-test
request legitimately belongs to `test-strategy`). The negative was corrected to a CI-timeout scenario
outside the skill's domain and the final pass scored **42/42**.

## Behavioral results

| Skill | Eval | Assertions | Result | Evidence highlight |
| --- | --- | ---: | --- | --- |
| feature-interrogation | vague-ai-recommendations | 6/6 | PASS | LEARN FIRST; no code; alternatives incl. do nothing; 2-week concierge test; kill criteria |
| simplest-solution | minimal-currency-and-cache | 5/5 | PASS | `Intl.NumberFormat`; 0 deps; rejected speculative cache; complexity budget |
| acceptance-criteria | team-invitations-contract | 6/6 | PASS | 33 observable rules; expiry boundary; revoke/resend races; non-goals; DoD |
| code-review | pre-ship-server-review | 6/6 | PASS | 5 P0 + 5 P1 with `file:line`; SQLi, authz, secrets, hash leak, N+1 |
| debug-root-cause | cart-concurrency-bug | 5/5 | PASS | Shared module state; per-user fix; concurrency regression test fails on old code |
| refactor-safely | utils-behavior-preserving-cleanup | 5/5 | PASS | 16 characterization tests; 443-case differential harness; 0 mismatches |
| test-strategy | risk-based-test-plan | 6/6 | PASS | P0 auth/data-integrity; real Postgres; cart concurrency; explicit not-testing list |
| security-review | pre-internet-security-audit | 6/6 | PASS | 6 critical findings; threat model; actor/impact/evidence/fix/verification |
| performance-engineering | orders-api-performance | 6/6 | PASS | Honest baseline; N+1 proof; join/limit; index left unapplied with reason; harness |
| migration-safety | live-orders-status-migration | 6/6 | PASS | Expand/contract; `lock_timeout`; concurrent index; batched backfill; rollback |
| api-contract | partner-orders-api-contract | 6/6 | PASS | RFC 9457; cursor pagination; idempotency; minor-unit money; 17 breaking changes |
| anti-ai-slop | remove-slop-from-readable-surfaces | 6/6 | PASS | Spanish; fake proof removed; purple gradient/three cards; asks for missing facts |
| clear-writing | readme-and-error-rewrite | 5/5 | PASS | Runnable README; dotenv absence found; errors say cause + next action |
| pr-craft | split-messy-working-tree | 6/6 | PASS | Two branches; formatting isolated; PII debug log removed; why/verify/risk/rollback |
| accessibility-audit | signup-form-wcag-22-aa | 6/6 | PASS | Real form/button; labels; error summary; contrast math; target size; reduced motion |
| design-system-discipline | minimal-token-system-migration | 6/6 | PASS | 3 token layers; 85/85 tokens consumed; states; no redesign; no unused variants |
| motion-quality | purposeful-dashboard-motion | 6/6 | PASS | Purpose table; 90/150/220ms; transform/opacity; reduced motion; pulse removed |
| observability-first | on-call-debuggability | 6/6 | PASS | Structured logs; trace context; RED/USE/business metrics; SLO burn alerts; drill |
| release-readiness | friday-signup-and-migration-go-no-go | 6/6 | PASS | NO-GO; signup is inert; migration unsafe; no artifact; owners/abort criteria |
| dependency-hygiene | package-json-audit | 6/6 | PASS | Remove 5; upgrade JWT; platform replacements; lockfile/install-script/license risk |
| image-to-ui | pixel-level-dashboard-reproduction | 7/7 | PASS | 1440×900 DPR 1; measured tokens; render+diff; 2.5566% mismatch; deviations explained |

## Notable verification details

- **Static analysis scripts were exercised both ways.** `scan_slop.py` found 27 candidates in the
  fixture and 0 after the anti-slop rewrite; `scan_a11y.py` found 1 high + 3 medium before the a11y
  fix and 0 after; `perf_gate.py` correctly failed a +23.8% LCP regression; `image_probe.py` returned
  0.0000% on an exact copy and failed a shifted/color-changed render at 10.1%.
- **`image-to-ui` produced a real render, not a claim.** The final diff was 33,133 px (2.5566%) at
  tolerance 8/255, with card edges, table rules, column starts, and control bounds within 0–1 px. The
  remaining differences are small-text antialiasing, hand-reconstructed icons, and the Georgia
  wordmark; the report explicitly does **not** call it pixel-perfect.
- **The UI fixture is real.** `evals/fixtures/ui-reference/reference.png` is a 1440×900 screenshot
  generated from a static page. The source markup is kept in `evals/fixtures/ui-reference-src/` for
  reproducibility and is not copied into the eval run.
- **No skill needed a body rewrite after testing.** The only correction was a mislabeled negative
  trigger, which is test data, not skill behavior.

## Platform coverage for `image-to-ui`

| Target | Status |
| --- | --- |
| Plain HTML/CSS | **Behaviorally tested** (same viewport, render, diff) |
| React/Next, Vue/Nuxt, Svelte/SvelteKit, Angular, Tailwind, CSS-in-JS | Recipes documented in `references/frameworks.md`; not yet rendered/diffed |
| Flutter | Golden-test recipe documented; SDK is installed, but the full reference has not been run |
| SwiftUI/UIKit | **Capture pipeline smoke-tested**: `ImageRenderer` rendered 320×180 @2x → 640×360 PNG, read by `image_probe.py`; full reference not run |
| React Native / Expo | Detox/Maestro/simctl/adb recipe documented; not yet run |
| Jetpack Compose / Android Views | Paparazzi/Roborazzi/screencap recipe documented; no Android toolchain in this environment |
| .NET MAUI / desktop shells | Harness guidance documented; not yet run |

This machine has Flutter, Swift, Xcode, and an iOS simulator available; Android tooling was not
installed. A platform is "supported" only after the reference image is rendered and diffed on it,
so the table separates verified from documented.

## Limitations

- No baseline (no-skill) control runs. The suite measures whether the skill produces the intended
  behavior, not the lift over an unassisted model. That is the next experiment if needed.
- Fixture runs are static/local; they do not execute a real Postgres, browser accessibility tree, or
  production traffic. Reports mark those gaps explicitly.
- Trigger tests use a router simulation with metadata only; real clients also weigh context and
  conversation history.
- `evals/runs/` is gitignored. The reports and artifacts are local evidence; this file is the durable
  summary.

## Reproduce

```bash
python3 evals/build-evals.py
python3 evals/setup_runs.py
python3 scripts/validate-skills.py
# then run each evals/evals.json prompt with an agent that loads the skill
```
