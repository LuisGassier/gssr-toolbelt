---
name: anti-ai-slop
description: "Detect and remove AI slop from code, UI, copy, docs, tests, and PRs: generic naming, comment noise, over-abstraction, fake data, hedging, emoji headers, purple-gradient sameness, and seamless/robust/leverage filler. Use whenever output feels generic, templated, bloated, or AI-generated, or before shipping anything a human will read. Replaces slop with specific, earned choices instead of swapping one template for another."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: craft
  standard: agentskills.io
---

# Anti-AI-Slop

Slop is not a vocabulary problem. It is the absence of a specific decision. The words
"seamless" and "robust" are symptoms; the disease is that the writer did not know who the
user is, what the product does, or why this choice beats the alternative.

Removing slop therefore has three layers:

1. **Substance** — does this say anything true and useful?
2. **Specificity** — does it name the user, the number, the constraint, the trade-off?
3. **Craft** — is it consistent, restrained, and shaped for its reader?

If you only run a word blacklist, you will produce sterile text that still says nothing.
Fix the substance first, then the surface.

## Non-negotiables

- **Do not invent proof.** No fake testimonials, logos, customer counts, uptime numbers, or
  benchmarks. If you do not have data, say what is true and what is unknown.
- **Do not add decoration to hide emptiness.** Gradients, glassmorphism, emoji, and animation
  cannot substitute for a clear hierarchy or a real value proposition.
- **Prefer one specific claim to three generic ones.** "Cuts invoice reconciliation from 40
  minutes to 6" beats "streamlines your workflow".
- **Match the register to the product.** A banking tool and a children's app should not share
  the same voice; both can be specific.
- **Delete before rewriting.** Remove whole sections that exist only to fill a template.

## Workflow

### 1. Identify the artifact and its reader

| Artifact | Reader | What specificity looks like |
| --- | --- | --- |
| README | Evaluator, new contributor | What it does, for whom, how to run it, real limits |
| Landing page | Prospective user | Concrete outcome, real proof, next action |
| UI copy | User in a task | What happened, what to do, what it costs |
| Error message | Stuck user/developer | Cause, fix, where to look next |
| Code | Maintainer | Domain names, obvious control flow, no ceremony |
| Test | Future debugger | The behavior and the failure it protects |
| PR | Reviewer | Why, what changed, risk, verification |
| Docs | Implementer | Exact steps, versions, gotchas |

### 2. Find the slop

Scan for these families. Use `scripts/scan_slop.py` for a first pass, then read the artifact.

**Substance slop**

- Claims with no evidence: "trusted by thousands", "99.9% uptime", "industry-leading".
- Fake specificity: "10x faster" with no baseline, "AI-powered" with no model or task.
- Placeholder people and companies presented as real: John Doe, Acme Corp, "Sarah from
  Finance".
- Sections that restate the heading or each other.
- Features described by adjective instead of behavior.

**Specificity slop**

- "Users can…" without saying which user, under what condition.
- "Fast", "secure", "simple", "modern", "powerful" with no number or example.
- Generic names: `data`, `item`, `manager`, `service`, `utils`, `helpers`, `handleData`.
- Comments that repeat the code: `// increment i`.
- Tests named `test1`, `works`, `should work`.

**Craft slop**

- Purple/indigo gradient + white card + three equal feature columns.
- Emoji as section headers (🚀 Features, ✨ Benefits).
- Every element rounded, shadowed, and animated with the same intensity.
- Hedging: "it's worth noting", "generally speaking", "in today's fast-paced world".
- Filler transitions: "Moreover", "Furthermore", "In conclusion", "Let's dive in".
- Over-structuring: a 12-section README for a 200-line script.
- Over-commenting: JSDoc that translates the signature into English.
- Over-abstraction: interface + factory + registry for one implementation.
- Fake urgency: "Don't miss out", "Act now", countdowns that reset.

### 3. Decide: delete, replace, or keep

For each finding:

- **Delete** if it adds no information, no proof, and no usable instruction.
- **Replace** if there is a true, specific statement underneath. Ask the user for the missing
  fact rather than inventing one.
- **Keep** if it is plain but accurate. "Save changes" is not slop; it is clear.

Do not replace a generic phrase with a synonym. "Seamless" → "effortless" is still slop.
"Seamless" → "imports a CSV and reconciles it in one pass" is a fix.

### 4. Rewrite by layer

**Code**

- Rename to domain language: `reservation`, `invoice`, `retryAfterMs`, not `data2`.
- Remove wrappers that only forward arguments. Call the thing directly.
- Delete dead options, unused params, speculative interfaces, and commented-out code.
- Replace generic `utils` dumping grounds with a named module or local function.
- Make comments explain *why* (constraint, workaround, invariant), not *what*.
- Prefer the framework/platform idiom over a bespoke mini-framework.
- Keep error messages specific: what failed, with what input, what to do.

**UI**

- Replace the default gradient-card layout with a composition driven by the product's
  content: a table for records, a timeline for events, a document for reading.
- Use one accent color with intent, not a rainbow of gradients.
- Remove decorative icons that do not aid recognition; keep functional ones.
- Use type scale and spacing to create hierarchy instead of borders and shadows everywhere.
- Write real empty states: what this is, why it is empty, what to do next.
- Use real data shapes in mockups (names, dates, amounts) or clearly label placeholders.
- Motion only where it clarifies cause/effect or continuity.

**Copy and docs**

- Lead with the outcome: what the reader gets, in one sentence.
- Replace adjectives with numbers, names, or examples.
- Cut hedges, intensifiers, and throat-clearing.
- Use the reader's words, not internal jargon.
- One idea per paragraph; short sentences; active voice.
- Delete the intro that explains what the document will explain.
- Keep a human voice; specificity is not the same as coldness.

**Tests**

- Name the behavior and condition, not `testWorks`.
- Assert the observable outcome; remove assertions on private calls.
- Delete tests that only exercise the framework or duplicate a stronger test.
- Replace sleep/retry hacks with deterministic waits.

### 5. Verify like a skeptical reader

Read the result aloud and ask:

- Could this describe ten other products? If yes, it is still generic.
- Is every number sourced? If not, remove it or label it as an example.
- Does every section earn its space?
- Would a real user know what to do next?
- Is the tone consistent across screens/docs/errors?
- Did I remove personality along with slop? Add one true, specific detail back.

## Severity guide

| Severity | Examples | Action |
| --- | --- | --- |
| High | Fake proof, invented metrics, misleading claims, placeholder data presented as real | Remove or source before shipping |
| Medium | Generic naming, filler copy, over-abstraction, comment noise | Fix in the touched area |
| Low | Emoji headers, redundant transitions, cosmetic clichés | Clean up if cheap; do not churn |

## Gotchas

- **Slop detection has false positives.** "Robust" can be legitimate in a technical sense
  (robust to malformed input). Read the sentence, not just the word.
- **Minimalism can be its own template.** A page of gray text with one accent is not
  automatically tasteful; it still needs hierarchy and a point of view.
- **Do not rewrite user-provided copy without permission** if it carries legal, brand, or
  compliance meaning. Flag it and propose.
- **Fake specificity is worse than honest generality.** "40% faster" invented on the spot is
  a lie; "faster on large imports, benchmark pending" is honest.
- **Code slop can be load-bearing.** A weird workaround may encode a production bug. Ask
  before deleting; add a test if you keep it.
- **Localization changes the tells.** Emoji and slang may be appropriate in one market and
  wrong in another. Match the audience.
- **The scan is a prompt, not a verdict.** A clean scan does not mean the artifact is good.

For the full pattern catalog with replacements, read
[references/slop-patterns.md](references/slop-patterns.md).

## Using the scanner

```bash
python scripts/scan_slop.py . --fail-on high
python scripts/scan_slop.py README.md src/ --json
```

The scanner is conservative and heuristic. Treat findings as candidates for review, not
automatic edits. It skips lockfiles, vendored code, build output, and binaries.

## Output contract

```markdown
## What I changed
| Location | Slop | Replacement | Why |
| --- | --- | --- | --- |

## Deleted
- [Section/code] — [why it added nothing]

## Needs a fact from you
- [Claim] — [what number/source would make it credible]

## Left alone
- [Plain but accurate text] — [why it is not slop]
```

## Quality gate

- [ ] No invented proof, metrics, customers, or testimonials.
- [ ] Every generic claim was replaced with a specific fact, or deleted.
- [ ] Code names reflect the domain; no `utils` dumping ground in the touched area.
- [ ] Comments explain why, not what.
- [ ] UI choices are driven by content, not a template.
- [ ] Copy has no hedges, filler transitions, or emoji headers.
- [ ] Tests name behavior and assert outcomes.
- [ ] The result still has a human voice and a point of view.
