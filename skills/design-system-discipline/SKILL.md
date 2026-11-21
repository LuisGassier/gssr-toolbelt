---
name: design-system-discipline
description: "Keep UI coherent as it grows: token layers, primitives, variants, composition rules, deprecation, and migration of one-off styles. Use when adding components, reviewing UI consistency, cleaning up arbitrary values, building or extending a design system, or when a product starts to look like five different apps. Optimizes for consistent decisions, not for a component library with every possible prop."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: design
  standard: agentskills.io
---

# Design System Discipline

A design system is a set of decisions that stop being re-litigated on every screen. It is not
a component library with 80 props, and it is not a Figma file that drifts from the code. It is
the smallest set of tokens, primitives, and rules that makes the next screen obvious to build
and consistent with the last one.

## Non-negotiables

1. **Tokens are the only source of color, spacing, type, radius, shadow, and motion values.**
   No raw hex, arbitrary pixel, or one-off easing in feature code.
2. **Primitives before pages.** Fix the button/input/dialog once; do not restyle per screen.
3. **Variants are named by intent** (`primary`, `danger`, `ghost`, `compact`), not by
   appearance (`blue`, `big`, `rounded`).
4. **Composition over configuration.** Small composable pieces beat one component with 30
   boolean props.
5. **Every component has states**: default, hover, focus-visible, active, disabled, loading,
   error, empty, and dark mode where applicable.
6. **Deprecate in public.** Mark, migrate, and remove. Do not leave two ways to do the same
   thing forever.

## Workflow

### 1. Audit the current surface

Inventory what exists before adding:

- Colors, spacing, radii, shadows, fonts, and motion values actually used.
- Buttons, inputs, selects, dialogs, tabs, badges, cards, tables, toasts.
- Duplicated variants (`PrimaryButton`, `ButtonPrimary`, `CTAButton`).
- One-off styles in feature code (`#3B82F6`, `margin-top: 13px`, `border-radius: 11px`).
- Inconsistent states (some buttons have focus rings, some do not).
- Dark mode and responsive behavior.

Count usage. A token used once is a local decision; a value used 20 times is a system
decision. Do not promote everything.

### 2. Define token layers

Use three layers, from raw to semantic to component:

```
primitive:  --blue-600: #2563eb;  --space-4: 16px;  --radius-md: 8px;
semantic:   --color-action: var(--blue-600);
            --color-action-hover: var(--blue-700);
            --color-danger: var(--red-600);
            --surface-raised: var(--neutral-0);
component:  --button-primary-bg: var(--color-action);
            --button-primary-bg-hover: var(--color-action-hover);
```

Rules:

- Feature code uses **semantic/component** tokens, not primitives.
- Semantic names describe role, not value: `text-muted`, `surface-raised`, `border-strong`.
- Dark mode swaps semantic values, not every component.
- Keep the scale finite: spacing 4/8/12/16/24/32/48/64, not every integer.
- Type scale: a small set of sizes with line-height and weight paired.
- Motion tokens: duration fast/base/slow and easing standard/enter/exit.

### 3. Build primitives with variants

A primitive should cover the states and sizes the product actually uses:

| Component | Minimum API |
| --- | --- |
| Button | variant (primary/secondary/ghost/danger), size, loading, disabled, icon |
| Input | label, help, error, required, disabled, prefix/suffix |
| Dialog | title, description, close, footer actions, focus management |
| Tabs | items, selected, keyboard behavior |
| Toast | tone, message, action, dismiss, live region |
| Table | density, sortable header, empty/loading/error states |
| Badge | tone, size, icon |

Do not add a prop until at least two real screens need it. Do not add a variant that exists
only in a mockup.

### 4. Set composition rules

- Spacing comes from the scale; do not nest cards inside cards to create padding.
- One primary action per view; secondary actions are visually subordinate.
- Borders and shadows are not interchangeable; pick one elevation language.
- Focus ring is global and consistent; never remove it locally.
- Icons are sized from the type scale and align optically with text.
- Empty/loading/error states are part of the component, not an afterthought in the page.
- Responsive behavior is a property of the layout primitive, not ad-hoc media queries
  everywhere.

### 5. Migrate one-offs

Do not rewrite the whole app. Use the strangler pattern:

1. Add the token/primitive alongside the existing one.
2. Migrate the highest-traffic or highest-inconsistency screens first.
3. Codemod mechanical replacements (hex → token, spacing → scale).
4. Add a lint rule or scanner that rejects raw values in new code.
5. Remove the old primitive after the migration window.

Track the migration: files remaining, owner, deadline. A design system with no migration plan
becomes a third style.

### 6. Document and govern

- A live catalog (Storybook or equivalent) with every state, including error/empty/loading.
- Usage guidance: when to use, when not to, accessibility notes.
- A changelog for visual/behavioral changes.
- A contribution path: propose, review, add, deprecate.
- Visual regression tests for primitives.
- A clear owner; systems without owners rot.

## Decision rules

| Question | Default |
| --- | --- |
| New token or local value? | Local unless used in 3+ places with the same intent |
| New variant or new component? | Variant if it shares structure and behavior; new component if the interaction differs |
| New prop or composition? | Composition unless the prop is needed by 2+ real screens |
| Fix globally or locally? | Globally if it is a primitive defect; locally if it is a one-off layout need |
| Support dark mode now? | If the product ships dark mode, yes; otherwise design tokens so it can be added |
| Keep a deprecated component? | Only with a migration deadline and a lint warning |

## Gotchas

- **Token proliferation is the same disease as hardcoded values.** 60 semantic colors is not
  a system; it is a palette with extra steps.
- **Component APIs calcify.** Every prop is a promise. Start small; add on real demand.
- **Figma and code drift.** Treat code tokens as the source of truth, or generate both from
  one source.
- **Dark mode exposes hardcoded colors.** Audit with the theme switched, not by inverting.
- **Focus states are not optional.** A pretty button without a focus ring is broken.
- **Density variants multiply state coverage.** Each variant needs every state tested.
- **Overriding primitives in page CSS** recreates the inconsistency. Use props/variants or
  fix the primitive.
- **A design system does not fix weak hierarchy.** Consistent components can still produce a
  confusing page; composition and content still matter.

## Output contract

```markdown
## Audit
[Values/components duplicated, usage counts, inconsistency hotspots.]

## Proposed system
- Tokens: [layers and scale]
- Primitives: [components and variants]
- Composition rules: [...]
- States: [...]

## Migration
| Step | Scope | Verify |
| --- | --- | --- |

## Governance
[Catalog, lint/visual tests, owner, deprecation policy.]

## Deliberately not added
[Components/props/tokens deferred until real demand.]
```

## Quality gate

- [ ] Feature code uses semantic/component tokens, not raw values.
- [ ] Primitives cover all states used by the product, including focus and error.
- [ ] Variants are named by intent and limited to real needs.
- [ ] Dark mode/responsive behavior is token-driven, not per-page overrides.
- [ ] A migration path exists for one-offs and deprecated components.
- [ ] The catalog shows real content and edge states, not only the happy path.
- [ ] No new prop/variant without at least two real consumers.
- [ ] The system has an owner and a change process.
