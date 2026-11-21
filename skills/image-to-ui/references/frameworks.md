# Framework Mapping

The fidelity workflow does not depend on the framework: measure the image, express the
measured values as tokens, build the UI, render it at the exact viewport/DPR, diff, iterate.
What changes is **where the tokens live**, **how the component is composed**, and **how the
render is captured**.

Use this file when the target is React/Next, Vue/Nuxt, Svelte/SvelteKit, Angular, Tailwind,
CSS-in-JS, or an existing design system.

For Flutter, SwiftUI/UIKit, React Native, Jetpack Compose, Android Views, .NET MAUI, or desktop
shells, read [native-and-cross-platform.md](native-and-cross-platform.md).

## Principle: measure the DOM, not the source

The source of truth is the rendered pixels, not the JSX/SFC/template. A framework wrapper can
add a `div`, a host element, a scoped-style hash, or a default margin that changes geometry.
Always inspect the final DOM and the rendered box model.

If the target framework is not already in the repo, do not add one just to reproduce a
screenshot. Prefer the stack the product already uses.

## Pick the target stack explicitly

| Target | Token home | Component home | Screenshot harness |
| --- | --- | --- | --- |
| Plain HTML/CSS | `:root` custom properties | semantic HTML | Chrome headless / Playwright |
| React / Next | CSS variables, CSS Modules, or theme | JSX component + CSS | Playwright/Puppeteer, Storybook |
| Vue / Nuxt | CSS variables or scoped SFC styles | `.vue` SFC | Playwright, Storybook |
| Svelte / SvelteKit | CSS variables or component styles | `.svelte` | Playwright, Storybook |
| Angular | CSS variables / SCSS theme | component + template | Playwright, Storybook |
| Tailwind | `@theme` (v4) or `theme.extend` (v3) | utility classes + small components | same as host framework |
| CSS-in-JS | theme object / tokens | styled component or `css` prop | same as host framework |
| Design system | existing semantic tokens | existing primitives | same as host framework |

## Token mapping

Keep the three layers from the skill: primitive → semantic → component. The framework only
changes the syntax.

**Plain CSS**

```css
:root {
  --paper: #f8f5ef;
  --surface: #ffffff;
  --ink: #1d2a22;
  --border: #e3dccf;
  --accent: #c75b39;
  --radius-card: 8px;
}
```

**Tailwind v4**

```css
@import "tailwindcss";

@theme {
  --color-paper: #f8f5ef;
  --color-surface: #ffffff;
  --color-ink: #1d2a22;
  --color-border: #e3dccf;
  --color-accent: #c75b39;
  --radius-card: 8px;
}
```

**Tailwind v3**

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        paper: "#f8f5ef",
        surface: "#ffffff",
        ink: "#1d2a22",
        line: "#e3dccf",
        accent: "#c75b39",
      },
      borderRadius: { card: "8px" },
    },
  },
};
```

Rules:

- Promote measured values to tokens only when reused; a one-off 1px border can stay local.
- Do not round a measured 13px to the nearest Tailwind step and call it fidelity.
- If the project already has a token with the same role, use it and verify it matches; do not
  create a parallel token.
- Tailwind arbitrary values (`text-[10.8px]`, `w-[232px]`) are acceptable for measured one-offs
  but should be commented or promoted when repeated.

**CSS-in-JS**

```js
export const theme = {
  color: { paper: "#f8f5ef", surface: "#ffffff", ink: "#1d2a22", border: "#e3dccf", accent: "#c75b39" },
  radius: { card: "8px" },
  font: { display: 'Georgia, "Times New Roman", serif', ui: "-apple-system, BlinkMacSystemFont, sans-serif" },
};
```

Extract styles at build time where possible; runtime style injection can change order and
cause a flash that invalidates the screenshot.

## Component mapping

- **React/Next:** semantic JSX; `htmlFor` for labels; `useId` for unique ids; avoid wrapper
  `div`s that add layout; keep server/client markup stable to avoid hydration shifts.
- **Vue/Nuxt:** SFC `<template>` + `<style scoped>`; remember scope attributes add specificity;
  use `:deep()` sparingly; verify slot wrappers do not add margins.
- **Svelte:** component styles are scoped; `:global` only for deliberate global tokens; check
  that compiler output does not reorder selectors in a way that changes cascade.
- **Angular:** host elements are real boxes; check `display` defaults; use `:host` carefully;
  view encapsulation can change selector order.
- **Design systems:** compose existing primitives; override semantic tokens or documented
  variants, not internal class names. If a primitive cannot match the source without internal
  overrides, wrap it and document the deviation; do not fork the system for one screen.
- **Pages vs components:** reproduce the smallest unit the user asked for. A screenshot of a
  whole page may contain a reusable component; do not turn the page into a monolith.

## Screenshot harness

The reference is a rendered image. Capture the render with the same engine, viewport, DPR,
locale, and reduced-motion setting.

**Playwright**

```js
import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 1,
  colorScheme: "light",
  reducedMotion: "reduce",
  locale: "en-US",
  timezoneId: "UTC",
});
await page.goto("http://localhost:3000");
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: "render.png", animations: "disabled", caret: "hide" });
await browser.close();
```

**Puppeteer**

```js
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
await page.goto("http://localhost:3000", { waitUntil: "networkidle0" });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: "render.png", animations: "disabled" });
await browser.close();
```

Rules:

- Wait for fonts (`document.fonts.ready`), hydration, images, and any data fetch that changes
  layout. A screenshot taken too early is a false diff.
- Disable animations, caret, dev overlays, HMR badges, and scrollbars.
- Set the same DPR as the reference; otherwise geometry and glyphs cannot match.
- Use the same browser engine as the reference when possible; Chrome vs Safari vs Firefox
  differ in font rasterization and default form styles.
- Capture the element/page at the exact CSS viewport, not a resized full-page screenshot.

## SSR, hydration, and fonts

- Server-rendered HTML can differ from the hydrated DOM. Wait for hydration before capturing.
- Fonts loaded via `next/font`, `@font-face`, or a CDN need a `document.fonts.ready` wait; a
  fallback font changes line breaks and widths.
- Avoid layout shift: reserve image dimensions and font metrics (`size-adjust`,
  `font-display: optional` where appropriate).
- Next.js: use `next/font` or local fonts; avoid runtime CSS that depends on client state.
- Nuxt/SvelteKit: verify the SSR output and the hydrated output separately if the design
  depends on client state.
- Portals/modals render outside the component tree; screenshot after the portal is mounted.

## CSS delivery and cascade

- CSS Modules/scoped styles add hashes but should not change the declared values; verify the
  computed styles, not the class names.
- Tailwind purge/JIT can drop arbitrary classes used only in strings; keep class names static
  and visible to the scanner.
- Global resets can change default margins, line-height, and form controls; apply them
  deliberately and compare before adding.
- CSS custom properties inherit through Shadow DOM only if declared inside; design-system
  components using shadow roots need tokens passed explicitly.

## Framework-specific gotchas

- **React StrictMode** double-invokes effects in development; do not screenshot a development
  overlay or a double-mounted portal.
- **Next.js route transitions** can leave the previous page mounted; wait for the new route.
- **Vue scoped styles** add attribute selectors that can outrank global tokens; check cascade.
- **Svelte** may scope keyframes and selectors differently; verify the computed animation.
- **Angular** host elements and `display: inline` defaults can add unexpected boxes.
- **Tailwind** preflight resets headings/lists; the source may not use a reset. Compare.
- **CSS-in-JS** runtime insertion order can change a later override; use a deterministic order.
- **Design systems** may impose their own focus ring, spacing, or typography. If it conflicts
  with the reference, decide with the user: match the reference or preserve the system.

## Verification matrix

| Target | Status in this repo |
| --- | --- |
| Plain HTML/CSS | Behaviorally tested (`evals/runs/image-to-ui`) |
| React + Tailwind | Documented here; not yet behaviorally tested |
| Vue/Svelte/Angular | Documented here; not yet behaviorally tested |
| Design system composition | Guidance only |

If you test a framework variant, add an eval with:
- the same reference image,
- a runnable app/story at 1440×900 DPR 1,
- a Playwright/Puppeteer capture,
- the same `image_probe.py diff` threshold.

Do not claim framework parity from documentation alone; claim what was rendered and diffed.
