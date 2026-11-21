# UI reference

This folder contains the only source for the reproduction task:

- `reference.png` — 1440 × 900 CSS px at DPR 1, sRGB, PNG.

The screenshot was rendered in headless Chrome from a static page using system fonts
(Georgia for display, the platform sans for UI, Menlo/SFMono for numbers) and inline SVG
icons. No external images or fonts are required.

Reproduce it exactly at 1440 × 900 CSS px / DPR 1. The original source markup is deliberately
not included; measure the image. Do not substitute a different design, font, color, or layout
unless the image makes it impossible; state any substitution.

Deliver `index.html` and `styles.css` (plus assets if needed), a render at the same viewport,
and a diff report. Use the `image-to-ui` skill and its `image_probe.py` script.
