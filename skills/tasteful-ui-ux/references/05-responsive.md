# Responsive Protocol

## 7. Responsive Behavior and Breakpoint Protocol

Responsive design is not a final cleanup step.

Every creation, improvement, and audit must consider mobile, tablet, and desktop behavior from the beginning.

Do not assume that a layout is responsive because it uses flexible units, Tailwind breakpoints, CSS Grid, or a component library. Responsive quality must be designed intentionally.

### Responsive Responsibility

For every interface, decide how the experience should adapt across:

- mobile
- tablet
- desktop
- wide desktop

Do not only resize the layout. Reconsider:

- content priority
- navigation behavior
- layout structure
- component density
- touch targets
- reading order
- scrolling behavior
- sticky elements
- empty space
- form usability
- table or data behavior
- chart behavior
- modal and drawer behavior
- image cropping
- CTA placement
- motion intensity

The mobile version is not a compressed desktop layout. It is the same experience re-prioritized for a smaller viewport.

### Breakpoint Thinking

Use breakpoints as design decisions, not as automatic layout switches.

Default viewport bands:

- Mobile: narrow, touch-first, single-column by default.
- Tablet: transitional space, often two-column but still touch-friendly.
- Desktop: full composition, richer layout, more parallel information.
- Wide desktop: preserve composition with max-widths, do not let content stretch endlessly.

Do not create a layout that only works at one viewport.

When using Tailwind defaults, assume:

- `sm`: small phones or larger mobile
- `md`: tablet and large mobile landscape
- `lg`: small desktop or large tablet
- `xl`: desktop
- `2xl`: wide desktop

Adjust to the project only when the existing system defines different breakpoints.

### Mobile-First Prioritization

On mobile, prioritize the user's next action.

Ask:

- What must the user understand first?
- What action matters most?
- What can be delayed, collapsed, hidden, or moved?
- What content becomes too dense?
- What interaction becomes hard to tap?
- What visual effect becomes noise?
- What desktop layout pattern breaks down?

Mobile should preserve clarity, not decoration.

Avoid:

- tiny tap targets
- horizontal overflow
- multi-column forms
- dense card grids
- small chart labels
- hover-only interactions
- sticky elements that consume too much height
- full-screen heroes that push the CTA below the fold
- desktop nav compressed into unreadable rows
- modals that are taller than the viewport

### Layout Collapse Rules

Every multi-column layout needs an explicit mobile collapse strategy.

For each section or component, decide:

- Does it collapse into one column?
- Does the visual move above or below the text?
- Does the CTA remain visible?
- Does the order need to change?
- Should some secondary content collapse into disclosure?
- Should cards become rows, accordions, tabs, or a carousel?
- Should data become summaries instead of full tables?

Do not rely on "it stacks automatically" as the responsive plan.

### Component-Specific Responsive Rules

#### Navigation

Desktop navigation must stay readable and intentional.

On mobile:

- Use a clear menu pattern when nav items do not fit.
- Keep primary action accessible.
- Avoid two-line nav bars.
- Avoid tiny nav links.
- Avoid hiding critical navigation without a replacement.

If the app has many sections or screens, consider sidebar, bottom nav, tabs, command menu, or contextual navigation based on product needs.

#### Hero or Top Section

The first viewport must communicate value quickly.

On mobile:

- Avoid huge headings that take the full screen.
- Keep the primary CTA reachable.
- Do not let decorative visuals push the message too far down.
- Crop or simplify hero media intentionally.
- Reduce secondary proof, metadata, or decorative text.
- Avoid `h-screen`; prefer stable viewport units such as `min-h-[100dvh]` when full-height behavior is needed.

#### Cards and Grids

Cards should not simply shrink until they become cramped.

On mobile:

- Convert multi-column grids to single-column lists when needed.
- Reduce card chrome if every item becomes visually heavy.
- Preserve the key comparison information.
- Avoid equal-height cards if content length varies heavily.
- Consider rows, grouped sections, tabs, accordions, or carousels when the content is not equally important.

#### Forms

Forms must remain easy to complete on touch devices.

On mobile:

- Use one column.
- Keep labels visible.
- Do not use placeholder text as the only label.
- Ensure error messages appear near the field.
- Make tap targets comfortable.
- Keep submit actions clear and reachable.
- Avoid multi-step complexity unless it improves comprehension.
- Use appropriate input types for keyboard behavior.

#### Tables and Data

Do not force desktop tables into mobile.

For dense data, choose a mobile pattern:

- priority columns
- stacked rows
- summary cards
- horizontal scroll with clear affordance
- expandable rows
- charts plus detail disclosure
- separate mobile-specific summary view

If the table is the product, preserve data access. If the table is supporting information, summarize first.

#### Charts and Metrics

Charts must remain legible.

On mobile:

- Reduce label density.
- Prioritize trend and interpretation.
- Avoid tiny legends.
- Move legends below or inline.
- Consider sparklines, summary panels, or key insights.
- Do not show a complex desktop chart if the user cannot read it.

#### Modals, Drawers, and Overlays

On mobile:

- Consider bottom sheets or full-screen dialogs instead of centered desktop modals.
- Keep close actions visible.
- Prevent body scroll conflicts.
- Ensure keyboard and focus behavior work.
- Avoid overlays that hide essential context unless the task is focused.
- Make destructive actions harder to trigger accidentally.

#### Motion

Motion should adapt to device and context.

On mobile:

- Avoid heavy parallax.
- Avoid hover-dependent motion.
- Avoid scroll hijacking unless truly justified.
- Reduce cinematic effects that hurt task speed.
- Prefer clear feedback, state transitions, and small tactile interactions.

Always respect reduced-motion preferences when motion is meaningful or repeated.

### Responsive Audit

When auditing responsive quality, check:

```text
Responsive audit:
- Mobile layout:
- Tablet layout:
- Desktop layout:
- Navigation behavior:
- Content priority:
- Touch targets:
- Overflow risks:
- Form usability:
- Data/table behavior:
- Media cropping:
- CTA visibility:
- Motion behavior:
- Accessibility risks:
- Highest-priority fixes:
```

### Responsive Output

When creating or improving UI, include responsive behavior in the output when relevant.

Use this format:

```text
Responsive plan:
- Mobile:
- Tablet:
- Desktop:
- Wide desktop:
- Key collapse rules:
- Components needing special handling:
- Main responsive risk:
```

### Responsive Failure Conditions

Treat these as failures:

- horizontal overflow on mobile
- desktop-only navigation
- unreadable text or chart labels
- tap targets that are too small
- CTAs hidden below unnecessary decoration
- forms that are hard to complete on mobile
- tables squeezed into unreadability
- modals that do not fit the viewport
- hover-only interactions with no touch equivalent
- layout order that stops making sense when stacked
- excessive whitespace caused by desktop spacing on mobile
- content stretching too wide on large desktop
- motion that causes jank, disorientation, or reduced usability

Fix these before considering the interface complete.
