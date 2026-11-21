---
name: accessibility-audit
description: "Audit and fix web accessibility to WCAG 2.2 AA: semantics, keyboard access, focus management, labels, contrast, forms, target size, motion, and ARIA restraint. Use when building or reviewing UI, when asked about a11y, accessibility, WCAG, screen readers, or keyboard navigation, or before shipping any user-facing screen. Prioritizes real user blockers over checkbox compliance."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: design
  standard: agentskills.io
---

# Accessibility Audit

Accessibility is not a compliance layer added at the end. It is whether a person using a
keyboard, a screen reader, a switch, voice control, or a magnifier can complete the task.
Automated tools catch roughly a third of issues; the rest require operating the interface.

Target **WCAG 2.2 Level AA** unless the product has a stricter obligation. Fix blockers
first: keyboard traps, missing names, unlabeled inputs, invisible focus, and unreadable
contrast.

## Non-negotiables

1. **Use native elements first.** `<button>`, `<a href>`, `<input>`, `<select>`, `<label>`,
   `<dialog>` come with keyboard and screen-reader behavior you cannot reproduce cheaply.
2. **Every interactive control is keyboard reachable and operable**, with a visible focus
   indicator that is not obscured.
3. **Every control has an accessible name**, and every input has a persistent visible label
   (placeholder is not a label).
4. **Do not use ARIA to patch broken semantics.** ARIA changes the announcement, not the
   behavior. No ARIA is better than wrong ARIA.
5. **Respect user preferences**: reduced motion, increased contrast, text scaling, and
   autoplay/pause.
6. **Test with the keyboard and at least one screen reader**, not only an automated scanner.

## Workflow

### 1. Scope the audit

List the screens/flows and the tasks a user must complete. Prioritize by:

- Revenue/critical path (signup, checkout, login, support).
- Forms and data entry (highest failure rate).
- Interactive components (menus, dialogs, tabs, comboboxes, drag-and-drop).
- Content-heavy pages (headings, landmarks, reading order).
- Motion/auto-updating content (carousels, toasts, live regions).

State what is out of scope. An audit of one flow is more useful than a vague "whole app".

### 2. Automated pass

Run the project's tooling if present (`axe`, `eslint-plugin-jsx-a11y`, Lighthouse,
Pa11y). Then run the bundled static scanner for common markup defects:

```bash
python scripts/scan_a11y.py src/ --fail-on high
```

Automation is a floor, not a ceiling. It will miss focus order, reading order, keyboard
traps, misleading labels, and cognitive load.

### 3. Keyboard pass

Put the mouse away and complete every task:

- Can you reach every control with `Tab`/`Shift+Tab` in a logical order?
- Is focus always visible, and not hidden behind a sticky header, footer, or cookie banner
  (WCAG 2.4.11)?
- Can you activate buttons/links with `Enter`/`Space` as expected?
- Can you escape dialogs, menus, and popovers with `Esc`?
- Is focus trapped inside a modal while open, and restored to the trigger when closed?
- Can you operate custom widgets: arrows in tabs/menus, `Home`/`End`, type-ahead?
- Are there keyboard traps anywhere?
- Can you skip repeated navigation (skip link) and reach the main content?
- Does focus order match visual order at every breakpoint?

### 4. Screen-reader pass

Use VoiceOver (macOS), NVDA (Windows), or TalkBack (Android) on the critical flow:

- Are headings announced in a useful hierarchy? Is there one `h1`?
- Are landmarks (`header`, `nav`, `main`, `footer`) present and named when repeated?
- Does every control announce a name, role, state, and value?
- Are form labels, required state, help text, and errors announced and associated?
- Are dynamic updates (toasts, validation, loading) announced without stealing focus?
- Are images meaningful (`alt`) or decorative (`alt=""`), not filenames?
- Are tables marked up with headers and captions where needed?
- Is reading order sensible when CSS reorders content?
- Are icon-only buttons named? Are decorative icons hidden?

### 5. Visual pass

- **Contrast:** 4.5:1 for normal text, 3:1 for large text (≥24px regular or ≥18.66px bold);
  3:1 for UI components and graphical objects. Check hover/focus/disabled/placeholder states.
- **Text scaling:** at 200% zoom and 400% reflow, content remains usable without horizontal
  scrolling (except data tables/maps).
- **Text spacing:** increased line/letter/word spacing does not clip content.
- **Target size:** at least 24×24 CSS px (WCAG 2.5.8 AA), with spacing exceptions; 44×44 is a
  safer mobile default.
- **Color is not the only signal.** Errors, required fields, links, and chart series need a
  second cue.
- **Focus indicator** has sufficient contrast and area; do not remove outlines.
- **Dark mode** has its own contrast and state checks.

### 6. Forms and errors

- Every input has a visible `<label>` associated by `for`/`id` (or wrapping label).
- Required fields are marked in text, not only with `*` or color.
- Help text is associated via `aria-describedby`.
- Errors are announced, placed near the field, and explain how to fix the input.
- Error summary (for long forms) links to the fields.
- Do not clear the form on validation failure.
- Do not rely on `placeholder` for instructions; it disappears on input.
- Use `autocomplete` tokens for name, email, address, and passwords.
- Do not block paste in password/OTP fields.
- Provide a show-password option and allow password managers.
- WCAG 3.3.8: do not require a cognitive test for authentication unless an alternative
  exists (no puzzle captcha as the only path).

### 7. Motion and time

- Honor `prefers-reduced-motion` for non-essential animation.
- No content flashes more than three times per second.
- Auto-playing carousels/video: pause/stop/hide control; no autoplay with sound.
- Time limits can be extended or turned off, with a warning.
- Dragging interactions (sliders, sortable lists) have a non-drag alternative (WCAG 2.5.7).
- Sticky headers do not cover focused elements (WCAG 2.4.11).
- Loading states are announced; avoid indefinite spinners with no status text.

### 8. ARIA and custom widgets

- Prefer native semantics; use ARIA only when no native element fits.
- Follow the ARIA Authoring Practices pattern for the widget, including keyboard behavior.
- Required state: `aria-expanded`, `aria-selected`, `aria-checked`, `aria-current`,
  `aria-disabled`, `aria-busy` — update them with the visual state.
- `aria-hidden="true"` must never contain focusable content.
- `role="button"` on a `div` needs `tabindex="0"`, `Enter`/`Space` handling, and a name.
  Better: use a real `<button>`.
- Live regions: `aria-live="polite"` for status, `assertive` only for urgent errors; keep the
  region in the DOM before updating it.
- Dialogs: `role="dialog"`, `aria-modal="true"`, labelled, focus moved in and restored.
- Do not put `aria-label` on non-interactive elements unless it adds real context.

### 9. Report and fix

For each finding:

```
[Severity] WCAG criterion — issue
Where: screen/component/file
Who is blocked: keyboard / screen reader / low vision / cognitive / motor
Repro: steps
Fix: specific markup/behavior change
Verify: keyboard/screen-reader/contrast check
```

Severity:

- **Blocker:** task impossible for a group (keyboard trap, unlabeled input, invisible focus,
  unreadable contrast on primary action).
- **Major:** task possible but confusing/error-prone (missing error association, poor focus
  order, icon-only unlabeled control).
- **Minor:** polish (redundant ARIA, non-ideal alt text, small target within exception).

## Gotchas

- **`outline: none` without a replacement** removes the only focus cue. Use
  `:focus-visible` with a visible ring.
- **Placeholder as label** fails 1.3.1/3.3.2 and disappears exactly when the user needs it.
- **`aria-label` on a `<div>`** does nothing useful; it is not focusable and has no role.
- **`role="button"` without keyboard handlers** is a broken button. Native is cheaper.
- **Positive `tabindex`** breaks natural order; use `0`/`-1` and DOM order.
- **Focus management on route change** is required in SPAs; move focus to the new heading or
  main region and announce the page.
- **`aria-hidden` on a modal's background** is not enough; also trap focus and make the rest
  inert.
- **Toasts** need a live region; visually appearing text is not announced.
- **Color-only errors** fail for color-blind users; add text and an icon.
- **Zoom tests** at 200% often reveal fixed heights and clipped text.
- **Automated tools pass broken widgets.** A `div` with `role="button"` may pass axe and
  still be unusable by keyboard.

For the WCAG 2.2 AA checklist, read [references/wcag-22-aa.md](references/wcag-22-aa.md).

## Output contract

```markdown
## Scope
[Screens/flows, assistive tech used, what was not tested.]

## Blockers
### [WCAG x.x.x] [Issue]
- Where: [...]
- Blocked: [keyboard/screen reader/low vision/...]
- Repro: [...]
- Fix: [...]
- Verify: [...]

## Major
[...]

## Minor
[...]

## What works
[Controls/patterns that are already accessible, so they are not broken later.]

## Verification plan
[Keyboard, screen reader, contrast, zoom, reduced motion.]
```

## Quality gate

- [ ] Every interactive control is keyboard reachable/operable with visible focus.
- [ ] Every input has a persistent visible label and associated error/help text.
- [ ] Icons/images have correct alt semantics; decorative images are hidden.
- [ ] Contrast meets 4.5:1/3:1 in all states, including dark mode.
- [ ] Dialogs/menus manage focus and restore it on close.
- [ ] Dynamic status/errors are announced.
- [ ] Target size and dragging alternatives meet WCAG 2.2 AA.
- [ ] Reduced motion and zoom/text spacing were tested.
- [ ] ARIA is minimal, correct, and never replaces native semantics.
- [ ] Findings name who is blocked and include a verification step.
