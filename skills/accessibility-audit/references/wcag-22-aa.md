# WCAG 2.2 Level AA Checklist

Use for a structured audit. Criteria marked **2.2** are new in WCAG 2.2. Test with real
assistive technology; this list is a prompt, not a substitute for use.

## Perceivable

### 1.1 Text alternatives
- [ ] 1.1.1 Non-text content has a text alternative; decorative images use `alt=""`.
- [ ] Icon-only buttons have an accessible name; SVGs use `aria-hidden` or `<title>`.
- [ ] Charts/diagrams have a text summary or data table.
- [ ] Captchas have an alternative modality.

### 1.2 Time-based media
- [ ] 1.2.1 Audio-only/video-only has a transcript.
- [ ] 1.2.2 Prerecorded video has captions.
- [ ] 1.2.3 Audio description or full text alternative where needed.
- [ ] 1.2.4 Live captions for live audio; 1.2.5 audio description for video.

### 1.3 Adaptable
- [ ] 1.3.1 Semantic structure: headings, lists, tables, landmarks, form labels.
- [ ] 1.3.2 Meaningful reading order independent of CSS.
- [ ] 1.3.3 Instructions do not rely on shape, size, or location alone.
- [ ] 1.3.4 Orientation is not locked to portrait/landscape.
- [ ] 1.3.5 Input purpose is identified (`autocomplete` tokens).

### 1.4 Distinguishable
- [ ] 1.4.1 Color is not the only means of conveying information.
- [ ] 1.4.2 Audio can be paused/stopped or has volume control.
- [ ] 1.4.3 Contrast: 4.5:1 normal text, 3:1 large text.
- [ ] 1.4.4 Resize text to 200% without loss of content/function.
- [ ] 1.4.5 Images of text avoided (except logos).
- [ ] 1.4.10 Reflow at 320 CSS px width / 400% zoom without 2D scrolling.
- [ ] 1.4.11 Non-text contrast: 3:1 for UI components and graphics.
- [ ] 1.4.12 Text spacing: no clipping when spacing is increased.
- [ ] 1.4.13 Content on hover/focus is dismissible, hoverable, persistent.

## Operable

### 2.1 Keyboard
- [ ] 2.1.1 All functionality is keyboard operable.
- [ ] 2.1.2 No keyboard trap; focus can leave every component.
- [ ] 2.1.4 Single-character shortcuts can be turned off/remapped or are focus-only.

### 2.2 Enough time
- [ ] 2.2.1 Time limits can be turned off/adjusted/extended with a warning.
- [ ] 2.2.2 Moving/blinking/auto-updating content can be paused/stopped/hidden.

### 2.3 Seizures
- [ ] 2.3.1 Nothing flashes more than three times per second.

### 2.4 Navigable
- [ ] 2.4.1 Skip link / bypass blocks.
- [ ] 2.4.2 Page has a descriptive title.
- [ ] 2.4.3 Focus order is logical and matches visual order.
- [ ] 2.4.4 Link purpose is clear from text/context; no "click here".
- [ ] 2.4.5 Multiple ways to find pages (nav, search, sitemap).
- [ ] 2.4.6 Headings and labels describe topic/purpose.
- [ ] 2.4.7 Focus is visible in every state.
- [ ] **2.4.11 (2.2)** Focused element is not entirely obscured by sticky headers/footers/
      cookie banners.
- [ ] 2.4.12 (AAA) Focus not obscured at all; aim for it on critical controls.
- [ ] 2.4.13 (AAA) Focus appearance: area and contrast; use a clear ring.

### 2.5 Input modalities
- [ ] 2.5.1 Pointer gestures have a single-pointer alternative.
- [ ] 2.5.2 Pointer cancellation: activation on up-event, undo where possible.
- [ ] 2.5.3 Accessible name contains the visible label text.
- [ ] 2.5.4 Motion actuation (shake/tilt) has a UI alternative and can be disabled.
- [ ] **2.5.7 (2.2)** Dragging movements have a non-drag alternative (buttons, inputs).
- [ ] **2.5.8 (2.2)** Target size at least 24×24 CSS px, or sufficient spacing/exception.
- [ ] 2.5.5 (AAA) Target size 44×44 for touch; recommended.

## Understandable

### 3.1 Readable
- [ ] 3.1.1 Page language is set (`<html lang>`).
- [ ] 3.1.2 Language changes within content are marked.

### 3.2 Predictable
- [ ] 3.2.1 Focus does not trigger a change of context.
- [ ] 3.2.2 Changing a field does not auto-submit without warning.
- [ ] 3.2.3 Navigation is consistent across pages.
- [ ] 3.2.4 Components with the same function are identified consistently.
- [ ] **3.2.6 (2.2)** Help mechanisms (contact, chat, FAQ) appear in a consistent order.

### 3.3 Input assistance
- [ ] 3.3.1 Errors are identified in text and described.
- [ ] 3.3.2 Labels or instructions are provided for input.
- [ ] 3.3.3 Error suggestion is provided when known.
- [ ] 3.3.4 Error prevention for legal/financial/data changes: review, confirm, or undo.
- [ ] **3.3.7 (2.2)** Redundant entry is not required in the same process (autofill/reuse).
- [ ] **3.3.8 (2.2)** Authentication does not rely on a cognitive test; paste and password
      managers are allowed; an alternative exists.

## Robust

### 4.1 Compatible
- [ ] 4.1.1 Valid, parseable markup (no duplicate IDs, no broken nesting).
- [ ] 4.1.2 Name, role, value exposed for all UI components; states update.
- [ ] 4.1.3 Status messages are announced via live regions without moving focus.

## Component patterns to test

- **Modal dialog:** labelled, focus moved in, trapped, `Esc` closes, focus restored.
- **Menu/dropdown:** arrow keys, `Home`/`End`, `Esc`, type-ahead, `aria-expanded`.
- **Tabs:** arrow keys, `aria-selected`, panel association, focus management.
- **Combobox/autocomplete:** input role, listbox, `aria-activedescendant`, announcements.
- **Accordion:** button + `aria-expanded`, content association.
- **Toast:** `role="status"`/`aria-live="polite"`, dismissible, not focus-stealing.
- **Data table:** `<th scope>`, caption, sortable state announced.
- **Carousel:** pause/stop, no autoplay with motion, controls named, no focus trap.
- **Drag-and-drop:** keyboard alternative, grab/drop announcements.
- **Form validation:** error association, summary, focus to first error, no data loss.
