# Fidelity Checklist and Measurement Notes

Use with image-to-ui. Measure at 100% and zoom to 200–800%; sample flat regions, never
antialiased edges.

## 1. Coordinate system and DPR

- Read the image dimensions in pixels (`image_probe.py info`).
- Infer CSS viewport: `css_px = image_px / DPR`.
- Common DPRs: 1, 1.5, 2, 3. A 2880px-wide screenshot is usually 1440 CSS px at 2×.
- If the screenshot includes browser chrome, subtract it before inferring the content box.
- Render at the same CSS viewport and DPR; otherwise geometry and glyphs will not line up.
- Check whether the image is a crop: no browser chrome, cut-off content, or non-standard
  aspect ratio are signals. Ask for the full frame.

## 2. Geometry

For each region, record x, y, width, height, and the gap to its neighbors.

- Draw a grid every 8px and every 100px; see which edges snap.
- Measure from border box edges, not from text glyphs.
- Check whether the layout is centered, left-aligned, or uses a max-width container.
- Measure gutters, not just column widths.
- Record minimum and maximum widths; note where content wraps.
- Check for optical alignment: icons often sit 1–2px above the text baseline; badges may be
  vertically centered to the cap height, not the line box.

## 3. Typography

- **Family:** identify by skeleton, terminals, and contrast. Compare candidate fonts at the
  same size. Serif vs sans is not enough.
- **Size:** measure cap height or x-height and convert with the font's metrics. If unavailable,
  estimate from known UI text and verify by line breaks.
- **Weight:** compare stroke thickness at the same size; 400 vs 500 is often visible in
  small text, 600 vs 700 in headings.
- **Line-height:** distance between baselines of consecutive lines. Do not use a default.
- **Letter-spacing:** compare word width to the font's natural advance; negative tracking is
  common in display type, positive tracking in uppercase labels.
- **Case and features:** uppercase transforms, small caps, tabular numerals, ligatures,
  slashed zero, old-style figures.
- **Color and opacity:** sample the interior of thick strokes, not edges.
- **Wrapping/truncation:** record exact line breaks, max lines, ellipsis, and hyphenation.
- **Font smoothing:** macOS/Chrome renders differently from Windows/Linux; do not chase
  glyph-level diffs before geometry and color match.

## 4. Color

- Sample 3–5 pixels inside a flat area; discard outliers.
- Avoid text, borders, shadows, gradients, and JPEG artifacts.
- Convert to sRGB for CSS; note if the source is Display P3.
- Check alpha: a color over a background is not the same as the composited result. Solve
  `result = alpha × fg + (1−alpha) × bg` when needed.
- Record hover/focus/disabled variants if visible.
- Check dark/light contexts separately.
- Use `image_probe.py palette` for the dominant colors, then verify each manually.

## 5. Borders, radii, shadows

- Border width: zoom to 800%; a 1px border is one device pixel at DPR 1, two at DPR 2.
- Border style: solid, dashed, dotted; inset vs outset; one side only.
- Radius: measure the horizontal and vertical extent of the curve; corners can differ.
- Shadows: estimate offset-x, offset-y, blur, spread, and color/alpha. Reproduce with
  `box-shadow: x y blur spread rgba(...)`; layer multiple shadows if the source has them.
- Inner shadows and inset highlights are common in tactile designs.
- Gradients: sample at least 3 stops; estimate angle; note hard stops and banding.
- Text shadows and glows: measure separately from box shadows.

## 6. Icons and imagery

- Prefer the original SVG if available; otherwise trace or recreate at the measured viewBox.
- Match stroke width (1, 1.5, 2), line caps (butt/round/square), joins, and fill vs outline.
- Match icon box size, not just the glyph; padding inside the viewBox affects alignment.
- For photos: crop at the exact aspect ratio and focal point; match border radius, overlay,
  and object-fit.
- For logos: use the real asset if licensed; do not approximate a trademark.
- For avatars: match size, shape, border, and fallback initials.
- For illustrations: recreate shapes or use a licensed equivalent; do not substitute a
  different style silently.

## 7. Content and states

- Transcribe copy exactly, including punctuation, capitalization, and line breaks.
- Match number/date/currency formatting and units.
- Reproduce visible states: active nav, selected tab/row, badge tone, disabled control,
  loading skeleton, empty state, error text, focus ring.
- Check truncation and overflow behavior.
- Check z-order: overlays, sticky headers, dropdowns, modals.

## 8. Responsive inference

- If only one viewport is provided, reproduce it exactly and document the inferred behavior.
- Use the source's spacing/type relationships to infer smaller/larger steps; do not invent a
  different design language.
- Decide what collapses, wraps, hides, or scrolls; list each decision.
- Test at least the target viewport plus one narrow and one wide viewport.
- If the image shows a fixed-width artboard, do not assume it is fluid.

## 9. Verification

- Render at the exact CSS viewport and DPR.
- Diff with `image_probe.py diff`; inspect the diff image, not just the percentage.
- Region-by-region check: header, sidebar, main, cards, table, footer.
- Fix geometry before typography, typography before color, color before micro-detail.
- Re-diff after each change; do not batch unrelated fixes.
- Compare at 100% for overall impression and 200–400% for detail.
- Record the final mismatch and remaining differences with reasons.
- If a difference is caused by font rendering or OS antialiasing, say so; do not claim a
  CSS bug you cannot fix.

## 10. Common failure modes

| Symptom | Likely cause |
| --- | --- |
| Everything is 2× too large | Forgot to divide image pixels by DPR |
| Text wraps differently | Wrong font metrics, size, width, or letter-spacing |
| Layout is 1–2px off everywhere | Border-box vs content-box, or box-sizing missing |
| 1px seams between blocks | Fractional widths/heights or zoom |
| Colors look close but wrong | Sampled an antialiased/compressed pixel, or P3 vs sRGB |
| Shadow looks heavier | Wrong spread/alpha or missing a second layer |
| Icons look off | Wrong stroke width, viewBox, or optical alignment |
| Page is wider than viewport | `100vw` with scrollbar, or a fixed width + padding |
| Diff is low but looks wrong | Structural/typographic error hidden by similar colors; inspect regions |
| Hover/focus missing | Only the static image was reproduced |

## 11. Minimal measurement sheet

```markdown
Canvas: 1440×900 CSS, DPR 1
Grid: 12 col, 24px gutter, 32px page padding
Sidebar: 232px, bg #14342B, border-right 1px #0E241D
Header: 64px, border-bottom 1px #E3DCCF
Display: Georgia 34/39, 400, -0.01em
Body: system-ui 14/20, 400
Label: system-ui 11/13, 600, 0.08em, uppercase
Card: #FFFFFF, radius 10px, border 1px #E3DCCF, shadow 0 1px 2px rgba(29,42,34,.06)
Accent: #C75B39
```
