---
name: image-to-ui
description: "Recreate a UI from a screenshot, mockup, or design image with pixel-level fidelity: measure geometry, typography, color, spacing, borders, shadows, assets, and states; build the interface; render and diff against the source; iterate until it matches. Use when asked to copy, clone, reproduce, or match a UI from an image, screenshot-to-code, pixel-perfect implementation, or to make a page look exactly like a design reference. The image is the specification, not inspiration."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: design
  standard: agentskills.io
---

# Image to UI

The image is the specification. Your job is to reproduce it, not to improve it, simplify it,
or impose your taste. If the reference uses a 13px label, a 1px border, an unusual serif, or
an asymmetric layout, that is a requirement until the person who provided it says otherwise.

"Pixel-perfect" is a claim that must be earned with a render and a diff. Eyeballing a
screenshot and writing plausible CSS is not reproduction; it is approximation.

## Non-negotiables

1. **Measure before you build.** Every color, size, gap, radius, and font property comes from
   the image or an explicit assumption, not from a default.
2. **Do not redesign.** No "cleaner" spacing, no different font, no new hierarchy, no
   removing elements because they seem decorative.
3. **Match the viewport and DPR.** A 1440×900 image at 2× is not the same as 1440×900 at 1×.
   Render at the source's CSS viewport and device pixel ratio.
4. **Reproduce the details.** 1px rules, optical alignment, line-height, letter-spacing,
   icon stroke width, shadow spread, gradient stops, and image crops are part of the design.
5. **Ask when the image is ambiguous.** Hidden states, responsive behavior, hover effects,
   and off-screen content cannot be invented. State the assumption or ask.
6. **Pixel fidelity does not excuse broken semantics.** Use real buttons, labels, headings,
   and alt text; flag inaccessible contrast or interaction in the source.

## Workflow

### 0. Establish the contract

Before measuring, confirm:

```
Source: [file/URL, resolution, color profile]
Viewport: [CSS width × height, inferred or given]
DPR: [1× / 2× / 3×, inferred or given]
Target stack: [plain HTML/CSS, React, Vue, Tailwind, ...]
Deliverable: [page, component, screenshot only]
States in scope: [default only / hover, focus, open, empty, error, ...]
Allowed deviations: [fonts, assets, responsive behavior, accessibility fixes]
Assets/licensing: [can crop from the image? are fonts/images licensed?]
```

If the viewport or DPR is unknown, infer it from the image and state the inference. Do not
silently assume 1440×900 at 1×.

### 1. Inspect the image forensically

Run the bundled probe first:

```bash
python scripts/image_probe.py info reference.png
python scripts/image_probe.py palette reference.png --colors 16
python scripts/image_probe.py grid reference.png --step 100 --out grid.png
python scripts/image_probe.py sample reference.png --points "24,24; 240,64; 400,300"
```

Then inspect at 100% and zoomed (200–800%) in an image editor. Record:

- **Canvas:** CSS width/height, DPR, visible browser chrome or crop edges.
- **Regions:** sidebar, header, main, cards, tables, footers; their bounding boxes.
- **Grid:** columns, gutters, max-width, alignment lines, baseline rhythm.
- **Type:** family, size, weight, line-height, letter-spacing, case, color, alignment.
- **Color:** exact fills, text, borders, shadows, gradients, overlays, opacity.
- **Geometry:** widths, heights, padding, margins, gaps, radii, border widths.
- **Elevation:** shadow offsets, blur, spread, color, and layering.
- **Assets:** icons (stroke/fill), illustrations, photos, logos, avatars, textures.
- **States visible:** active nav, selected row, badges, disabled controls, focus ring.
- **Content:** exact copy, truncation, line breaks, number formatting.

For measurement formulas and a detailed checklist, read
[references/fidelity-checklist.md](references/fidelity-checklist.md).

### 2. Build a measurement sheet

Do not go straight to code. Write the source of truth:

```markdown
## Canvas
1440 × 900 CSS px, DPR 1, background #F8F5EF.

## Layout
Sidebar 232px fixed, border-right 1px #DED6C7.
Header 64px, padding 0 28px, border-bottom 1px #E6DFD2.
Main max-width none, padding 28px 32px, column gap 24px.

## Type
Display: Georgia 34px/1.15, weight 400, letter-spacing -0.01em, #1D2A22.
Body: system-ui 14px/1.45, weight 400, #4A5148.
Label: system-ui 11px/1.2, weight 600, letter-spacing 0.08em, uppercase, #7A7468.
Mono: "SFMono-Regular", Menlo, 12px/1.4.

## Color
Paper #F8F5EF; surface #FFFFFF; ink #1D2A22; muted #6E756B;
accent #C75B39; forest #14342B; border #E3DCCF; verified #2F6B4F.
```

If a value is an estimate, mark it `~`. Do not mix measured and guessed values silently.

### 3. Implement in layers

1. **Structure:** semantic regions and landmarks first (`header`, `nav`, `main`, `aside`,
   `table`/list), not div soup.
2. **Layout:** the outer grid, widths, and alignment. Get the skeleton within 1–2px before
   styling details.
3. **Type:** load the closest licensed font. If the exact font is unavailable, match the
   metrics (x-height, width, weight) and state the substitution; do not pick a random
   "modern" font.
4. **Color and surface:** fills, borders, radii, shadows, gradients.
5. **Assets:** recreate icons at the measured stroke width and viewBox; crop photos at the
   exact aspect ratio; use SVG where the source is vector.
6. **States and content:** active/hover/focus/disabled/empty, exact copy and line breaks.

Use CSS variables for the measured tokens. Keep one-off values explicit rather than
inventing a scale the source does not use.

### 4. Render and compare

Render at the exact CSS viewport and DPR. For a static page:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1440,900 \
  --screenshot=render.png file:///absolute/path/index.html
```

Then diff:

```bash
python scripts/image_probe.py diff reference.png render.png \
  --out diff.png --overlay overlay.png --tolerance 8
```

Iterate in this order:

1. **Geometry:** block positions, widths, heights, gaps, alignment. Fix before color.
2. **Type:** font metrics, size, weight, line-height, letter-spacing, wrapping.
3. **Color:** fills, borders, text, gradients.
4. **Details:** radii, 1px lines, shadows, icon strokes, image crops, optical offsets.
5. **States:** hover/focus/active/disabled/empty.

Stop when the diff is within the agreed tolerance. If no tolerance was agreed, propose:
layout within 1px, text within 1–2px, flat colors within RGB Δ≤3, and no visible structural
difference at 100%.

### 5. Detail pass (the part most reproductions skip)

Check every item against the source at 200–400% zoom:

- Border widths: 1px vs 1.5px vs 2px; borders on one side only.
- Radii: each corner can differ; pills vs 6px vs 10px vs 24px.
- Shadows: offset-x/y, blur, spread, color/alpha, multiple layers.
- Gradients: angle, stops, midpoint, banding, overlay transparency.
- Type: cap height, x-height, baseline, line-height, tracking, tabular numbers, truncation.
- Optical alignment: icons vs text, badges vs baselines, avatars vs rows.
- Rules and dividers: inset vs full-bleed, opacity, dash patterns.
- Icons: stroke width, joins, caps, filled vs outlined, size, color.
- Images: crop, focal point, aspect ratio, border radius, overlay.
- Density: row heights, table padding, list gaps, control heights.
- Microcopy: punctuation, capitalization, units, dates, currency, ellipses.
- States: active tab, selected row, focus ring, disabled opacity, badge tone.
- Scrollbars, selection color, caret, placeholder, empty state (if visible).
- Background: flat vs subtle texture, noise, grain, gradient.

### 6. Responsive and hidden states

An image shows one state at one viewport. Do not invent the rest silently.

- If multiple breakpoints are provided, reproduce each and diff each.
- If only one is provided, implement a faithful version at that viewport and make the layout
  degrade sensibly; list the inferred breakpoints as assumptions.
- Do not reorder content or hide features without asking.
- For hover/focus/disabled states not shown, derive them from the visible design language and
  label them as inferred.
- If the image includes a cropped element, ask for the full design rather than guessing.

### 7. Accessibility and semantics

Pixel fidelity is visual, not an excuse to ship a `div` button.

- Use native elements (`button`, `a`, `input`, `label`, `table`, `nav`, `main`).
- Keep visible labels; if the source uses placeholder-only inputs, add an accessible label
  without changing the visual layout.
- Preserve contrast where possible; if the source fails WCAG, reproduce the look but flag the
  contrast and propose the smallest accessible adjustment.
- Ensure keyboard reachability and focus visibility, even if the screenshot does not show it.
- Add alt text for meaningful images; hide decorative ones.
- Do not add ARIA to compensate for non-semantic markup.

### 8. Deliver with evidence

```markdown
## Source
[Image, viewport, DPR, color profile, assumptions.]

## Fidelity
- Render: [size, DPR, browser]
- Diff: [pixel mismatch %, mean error, regions]
- Tolerance: [agreed/proposed]
- Remaining differences: [list with reason]

## Tokens
[Measured colors, type, spacing, radii, shadows.]

## Files
[index.html, styles.css, assets, screenshot, diff image]

## Inferred
[Responsive behavior, hover/focus/disabled states, fonts/assets substitutions.]

## Accessibility
[Semantics, labels, keyboard, contrast flags.]
```

## Fidelity levels

| Level | Requirement | Typical failure |
| --- | --- | --- |
| Structural | Same regions, grid, alignment, hierarchy | Invented spacing, reordered content |
| Visual | Same type, color, surfaces, imagery | Wrong font, guessed hex, wrong radius |
| Detail | Same 1px rules, shadows, icons, states | Missing dividers, wrong stroke width |
| Behavioral | Same interactions and responsive behavior | Only the static screenshot works |

Do not call it pixel-perfect at the structural level. Say which levels are verified.

## Gotchas

- **DPR confusion.** A 2× screenshot has twice the pixels; divide by DPR for CSS px. Use the
  same DPR when rendering or the diff will be meaningless.
- **Browser chrome is not UI.** Exclude tabs, URL bars, scrollbars, and OS window edges from
  the reproduction unless the task includes them.
- **Compression artifacts.** JPEG/WebP noise changes sampled colors. Sample flat areas away
  from edges and text; never sample an antialiased pixel as a fill.
- **Color profiles.** A P3 screenshot displayed in sRGB shifts colors. Convert deliberately
  and state the working space.
- **Font substitution changes everything.** A fallback with a different x-height or width
  breaks line breaks, alignment, and perceived weight. Match metrics or get the font.
- **Browser defaults.** Default margins, line-height, button padding, and form styles will
  drift from the design. Reset deliberately, not with a giant global `*` that hides the cause.
- **Subpixel rounding.** Fractional widths/heights can produce 1px seams. Use consistent
  rounding and check at 100% and 200%.
- **Viewport units include/exclude scrollbars.** `100vw` can be wider than the content box.
  Hide scrollbars only if the source did.
- **Text rendering differs across OS/browser.** Antialiasing and font smoothing change the
  diff even with identical CSS. Compare geometry first, then color, then glyphs.
- **The image may be stale.** It can show content, states, or features the product no longer
  has. Confirm the source of truth before reproducing a bug.
- **Licensing.** Do not lift copyrighted fonts, photos, or illustrations without permission;
  use a licensed match and say so.
- **Do not "fix" the design silently.** If the source has an accessibility or usability
  problem, reproduce it and flag it; the client decides.

## Output contract

For a page or component, deliver:

1. The implementation files (HTML/CSS/JS or framework components).
2. The exact render at the source viewport/DPR.
3. The diff image and numeric mismatch.
4. The measurement sheet/tokens.
5. A list of inferred behavior (responsive, states, font/asset substitutions).
6. Accessibility notes and any deliberate deviations.

## Quality gate

- [ ] Viewport and DPR are known and the render uses them.
- [ ] Layout geometry is within 1px of the source (or the agreed tolerance).
- [ ] Type uses measured size/weight/line-height/letter-spacing; font substitution is stated.
- [ ] Colors are sampled from flat areas, not guessed.
- [ ] 1px rules, radii, shadows, gradients, and icon strokes match at 200% zoom.
- [ ] Exact copy, line breaks, units, and number formatting match.
- [ ] Visible states (active, selected, badge, disabled) are reproduced.
- [ ] Hidden/responsive states are inferred explicitly, not silently invented.
- [ ] Semantics and keyboard access are correct despite visual fidelity.
- [ ] A diff image and mismatch number are provided; the fidelity claim matches the evidence.
