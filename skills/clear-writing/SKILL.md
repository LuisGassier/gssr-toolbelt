---
name: clear-writing
description: "Write technical prose that is specific, short, and useful: docs, PR descriptions, commit messages, error messages, UI microcopy, release notes, and incident updates. Use when writing or rewriting any text a human will read, when copy feels vague or corporate, or when an error message needs to tell someone what to do next. Optimizes for the reader's next action, not for sounding impressive."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: craft
  standard: agentskills.io
---

# Clear Writing

Clear writing is a design decision. The reader is in the middle of a task, has less context
than you, and is deciding whether to keep reading. Give them the point first, the detail they
need second, and nothing that only makes you sound thorough.

This skill is for technical prose: docs, READMEs, PRs, commit messages, errors, UI copy,
release notes, incident updates, and internal decision records. For marketing copy, keep the
same discipline but add a real value proposition and evidence.

## Non-negotiables

1. **Lead with the point.** First sentence says what this is, what happened, or what to do.
2. **Be specific.** Name the thing, the number, the condition, the version, the file.
3. **Write for the reader's next action.** If they cannot act after reading, the text failed.
4. **Cut anything that does not change understanding or behavior.** Length is not thoroughness.
5. **Use the reader's words.** Internal jargon and codenames need a definition or removal.
6. **Never fake certainty.** Mark assumptions, unknowns, and estimates honestly.

## Workflow

### 1. Name the reader and the job

```
Reader: [new contributor / on-call engineer / end user / reviewer / executive]
They need to: [run it / decide / fix an error / approve / understand a change]
After reading they should: [specific action or decision]
```

If you cannot fill this in, you are writing for yourself.

### 2. Choose the shape

| Artifact | Shape |
| --- | --- |
| README | What it is, who it is for, quickstart, configuration, limits |
| How-to | Prerequisites, numbered steps, verification, troubleshooting |
| Reference | Complete, scannable, consistent; no narrative |
| Explanation | Concept, why it matters, trade-offs, examples |
| PR description | Why, what, how verified, risk, rollback |
| Commit message | Imperative subject, why in the body, one logical change |
| Error message | What happened, why, what to do, where to look |
| UI microcopy | Outcome, constraint, next action; no cute ambiguity |
| Incident update | Impact, current status, next update time, what we need |
| Release note | User-visible change, migration/action required, date |

### 3. Draft with the point first

Use this order unless the artifact has a stronger convention:

1. **Answer / outcome** — one or two sentences.
2. **Why it matters / context** — only what changes interpretation.
3. **Details** — steps, options, edge cases.
4. **Next action** — what to do now, or where to go.

Avoid "In this document we will…" and "Before we begin, let's understand…". Start.

### 4. Tighten

Edit in passes:

- **Hedges:** remove "I think", "perhaps", "it seems", "generally", "arguably" unless the
  uncertainty is real and material.
- **Intensifiers:** remove "very", "really", "extremely", "highly", "truly".
- **Nominalizations:** "perform an analysis" → "analyze"; "make a decision" → "decide".
- **Passive voice:** use active when it clarifies who acts. Passive is fine when the actor is
  unknown or irrelevant.
- **Redundancy:** "past history", "future plans", "end result", "completely eliminate".
- **Throat-clearing:** delete the first paragraph if it only announces the document.
- **Jargon:** replace or define. Do not stack acronyms.
- **Lists:** use them for parallel items, not for prose chopped into bullets.
- **Sentences:** shorten. If a sentence has three commas and two "which", split it.
- **Examples:** replace an abstract claim with a concrete one.

### 5. Make errors actionable

Every user-facing error should answer:

```
What happened?   [specific, no error code alone]
Why?             [cause the user can understand]
What now?        [one action, or a support path]
What was kept?   [data not lost, retry safe, etc. — if true]
```

Bad: `Error: invalid input.`
Better: `The expiry date must be after today. Choose a date from tomorrow onward.`

Bad: `Something went wrong.`
Better: `We couldn't save your changes because the connection dropped. Your draft is still
here — retry when you're back online.`

Do not blame the user. Do not expose stack traces. Do not say "contact support" unless there
is a real support path and the user cannot fix it.

### 6. Write commit messages that survive

```
<type>(<scope>): <imperative summary, <= 72 chars>

Why this change is needed. What was wrong or missing.

What changed, at the level a reviewer needs. Note risky behavior,
migrations, flags, or follow-ups.

Refs: #123
```

- One logical change per commit.
- Subject in imperative mood: "add", "fix", "remove", not "added" or "adds".
- Body explains *why*, not a restatement of the diff.
- Do not use "WIP", "stuff", "minor fixes", or "address comments" as the final message.

### 7. Write PR descriptions for reviewers

```markdown
## Why
[Problem and user impact. Link the issue.]

## What
[Behavior change, not a file list.]

## How verified
- [Tests/commands and results]
- [Manual steps with inputs]

## Risk and rollback
[Blast radius, migration/flag, how to revert.]

## Screenshots
[Before/after for UI, with real data or labeled placeholder.]
```

Keep it proportional. A one-line fix needs a one-line why; a migration needs a timeline.

### 8. Review for the reader

- Read the first sentence alone. Does it tell the reader whether to continue?
- Read only the headings. Is the structure clear?
- Read only the code blocks/commands. Can they be run as written?
- Ask someone unfamiliar to follow it. Where do they hesitate?
- Check names, versions, links, and numbers. A wrong command is worse than no command.
- Remove the last paragraph if it only summarizes what was just said.

## Style rules

- Prefer short, concrete nouns and strong verbs.
- One idea per paragraph; 1–4 sentences is usually enough.
- Use "you" for instructions, "we" for team decisions, "the system" for behavior.
- Use present tense for current behavior, past tense for incidents.
- Use consistent terms; do not alternate synonyms for the same concept.
- Use sentence case for headings unless the product style says otherwise.
- Use numerals for measurements and counts; spell out only when it reads naturally.
- Define acronyms on first use.
- Link to the source of truth instead of copying it.
- Do not use emoji in technical docs unless the team already does.
- Do not use "simply", "just", "obviously", or "of course" — they punish the confused reader.

## Gotchas

- **Brevity can remove the why.** A terse instruction that omits a prerequisite is not clear.
- **Bullets can hide sequence.** If order matters, number the steps.
- **"User" is not an audience.** Name the role and the context.
- **Screenshots age.** Prefer text for steps; use images for layout, with alt text.
- **Translations change length.** UI copy should survive 30–40% expansion.
- **Error codes are not explanations.** Pair the code with a human sentence and a next step.
- **Legal/compliance copy is not yours to simplify.** Flag it; do not rewrite meaning.
- **Confidence and certainty are different.** "We have not reproduced this" is honest;
  "it is fixed" without verification is not.

## Output contract

For a rewrite, show:

```markdown
## Before
[Original, or the specific lines.]

## After
[Rewritten text.]

## What changed
- [Hedge removed / claim made specific / action added]

## Needs a fact
- [Claim that requires a number, source, or owner]
```

For a new document, deliver the document plus a one-line statement of reader and purpose.

## Quality gate

- [ ] The first sentence states the point.
- [ ] The reader and their next action are explicit.
- [ ] Every claim is specific or marked as an assumption.
- [ ] Hedges, filler, and redundant transitions are removed.
- [ ] Commands, links, versions, and names are correct and runnable.
- [ ] Errors say what happened, why, and what to do.
- [ ] The structure matches the artifact type.
- [ ] Nothing is repeated for the sake of length.
