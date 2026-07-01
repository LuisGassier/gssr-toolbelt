# System Consistency

## 8. Component and System Consistency Protocol

A polished interface is not a collection of individually styled pieces.

Every interface should feel like it belongs to one coherent product system.

When creating, improving, or auditing UI, evaluate whether the issue is local to one screen or caused by shared primitives, tokens, layout rules, or repeated patterns.

Do not fix the same visual or UX problem one instance at a time if it belongs in the system.

### System Awareness

Before changing components, inspect the available system evidence:

- existing component primitives
- design tokens
- CSS variables
- Tailwind config
- theme files
- global CSS
- shared layout wrappers
- typography utilities
- button variants
- input patterns
- card patterns
- navigation patterns
- modal/dialog patterns
- table/data patterns
- loading, empty, and error states
- accessibility helpers
- package.json dependencies

Use what already exists when it is good enough.

Improve or replace what exists when it is the source of weak UX, inconsistent visuals, poor accessibility, or generic AI-looking output.

Do not introduce a new visual language if the product already has a stronger one.

Do not preserve a weak system just because it exists.

### Local vs System-Wide Decision

Before changing a UI element, decide whether the fix should be local or system-wide.

A change is local when:

- the issue appears only in one specific context
- the component is intentionally unique
- the layout is specific to a page or flow
- changing the shared primitive would harm other use cases
- the user explicitly asks for a one-off treatment

A change is system-wide when:

- the same issue appears across multiple screens
- the problem comes from a shared primitive
- button, input, card, table, modal, or nav styles feel inconsistent
- spacing, typography, radius, color, or shadow rules are repeated incorrectly
- interaction states are missing from shared components
- accessibility issues come from the base component
- the product lacks a coherent visual language

If uncertain, inspect usage before deciding.

Do not silently turn a local request into a system-wide refactor if it could affect many screens. State the reason first.

Use this format when useful:

```text
System impact:
- Local issue or shared issue:
- Affected primitives:
- Affected screens:
- Recommended scope:
- Risk:
- Reason:
```

### Primitive Component Standards

Foundational primitives define the product feel.

Treat these as system-level unless the user says otherwise:

- buttons
- links
- inputs
- textareas
- selects
- checkboxes
- radios
- switches
- sliders
- tabs
- menus
- cards
- dialogs
- drawers
- popovers
- tooltips
- tables
- badges
- toasts
- alerts
- empty states
- loading states
- navigation
- pagination
- breadcrumbs
- charts and metric blocks

When improving primitives, define the full behavior, not only the default state.

Each primitive should have appropriate:

- default state
- hover state
- active state
- focus-visible state
- disabled state
- loading state, when relevant
- selected state, when relevant
- error state, when relevant
- empty state, when relevant
- reduced-motion behavior, when relevant
- light and dark behavior, when relevant
- mobile and touch behavior, when relevant

A primitive that only looks good in its default state is unfinished.

### Component API Preservation

When modifying existing components, preserve the component contract unless the user approves a breaking change.

Do not silently break:

- prop names
- variant names
- exported component names
- event handlers
- form behavior
- validation behavior
- accessibility attributes
- keyboard behavior
- analytics hooks
- test selectors
- route behavior
- data loading behavior

If the current API prevents a better design, propose a migration instead of forcing a silent rewrite.

Use this format when useful:

```text
Component contract:
- Preserve:
- Needs change:
- Breaking risk:
- Migration recommendation:
```

### Variant Discipline

Do not create random one-off variants.

For each primitive, keep variants clear and purposeful.

Button example:

- primary
- secondary
- tertiary or ghost
- destructive
- link
- icon-only

Input example:

- default
- error
- disabled
- read-only
- with helper text
- with leading or trailing affordance

Card example:

- basic container
- interactive card
- metric card
- media card
- alert or status card
- dense list item

Avoid variant sprawl.

If two variants communicate the same hierarchy, merge them.

If a variant exists only because one screen needed decoration, remove it or make it local.

### Token Discipline

Use tokens or shared values for repeated visual decisions.

System-level decisions should not be scattered as arbitrary values.

Evaluate and standardize:

- color tokens
- typography scale
- font families
- font weights
- line heights
- spacing scale
- radius scale
- border treatment
- shadow/elevation scale
- z-index layers
- motion durations
- easing curves
- breakpoints
- container widths

Do not invent new values unless the existing scale cannot express the needed design.

Avoid arbitrary styling that cannot be explained:

- random radius values
- inconsistent shadow strengths
- multiple accent colors without a rule
- slightly different gray palettes
- different focus rings per component
- unrelated animation durations
- inconsistent padding across similar components

Every repeated visual decision should either use the system or become part of it.

### Design System Fit

If the project uses an existing design system or component library, respect its model.

Examples:

- shadcn/ui
- Radix Themes
- Material
- Fluent
- Carbon
- Polaris
- Atlassian
- Primer
- Bootstrap
- custom internal component system

Do not mix design systems casually.

Do not import a second system because one component looks convenient.

Do not leave imported components in their default visual state if the rest of the product has a custom direction.

Customize through the correct layer:

- tokens
- theme provider
- CSS variables
- component variants
- primitive wrappers
- global style rules
- documented utility classes

Avoid styling each instance manually when the library supports systematic theming.

### Consistency Without Sameness

Consistency does not mean every section, card, or component looks identical.

A good system creates recognizable rules with enough variation for hierarchy and context.

Maintain consistency in:

- typography logic
- spacing rhythm
- color behavior
- radius system
- interaction feedback
- icon style
- motion personality
- accessibility behavior

Allow variation in:

- layout composition
- section rhythm
- content structure
- emphasis
- density
- visual weight
- storytelling moments
- page-specific patterns

Do not solve inconsistency by making everything bland.

Do not solve generic design by making every component different.

### State and Feedback Completeness

Every interactive UI must communicate state.

Check for:

- hover feedback on pointer devices
- active or pressed feedback
- visible keyboard focus
- disabled state that still explains availability when needed
- loading state that matches final layout
- error state with clear recovery path
- empty state with useful next action
- selected state that is visually distinct
- success state when an action completes
- destructive action confirmation when appropriate

Do not use animation as a substitute for clear state.

Do not use color alone to communicate critical state.

### Accessibility as System Behavior

Accessibility should be built into primitives, not patched screen by screen.

System-level accessibility includes:

- semantic HTML
- keyboard navigation
- focus-visible styling
- ARIA only when needed
- sufficient contrast
- readable type sizes
- label and description relationships
- error association
- disabled and loading semantics
- reduced-motion support
- touch target size
- predictable tab order

If the shared primitive is inaccessible, fix the primitive.

Do not decorate inaccessible UI.

### Component Replacement

Do not assume the existing component is the right component.

Before refining a component, ask:

- What job is this component doing?
- Is this the right pattern for that job?
- Is the user comparing, scanning, deciding, configuring, reading, monitoring, or acting?
- Would a different component communicate better?
- Is this component repeated enough to become a system pattern?
- Is this a content problem, layout problem, interaction problem, or primitive problem?

Examples:

- A static stat card may need to become a trend panel.
- A dense settings form may need grouped sections or progressive disclosure.
- A generic feature card may need a product demo or proof block.
- A long list may need tabs, filters, grouping, or search.
- A modal may need to become an inline flow or drawer.
- A table may need a summary view on mobile.
- A badge may need to become a status system.

Do not preserve a component shape when the component shape is the problem.

### System Audit

When auditing a UI system, inspect:

```text
System audit:
- Existing primitives:
- Token consistency:
- Typography consistency:
- Spacing consistency:
- Color consistency:
- Radius and shadow consistency:
- Interaction states:
- Accessibility issues:
- Responsive behavior:
- Repeated AI-looking patterns:
- Local fixes needed:
- System-wide fixes needed:
- Highest-impact primitive to fix first:
```

### System Improvement Output

When making system-level improvements, summarize the system decision:

```text
System improvement:
- Problem source:
- Primitive or token affected:
- Current behavior:
- New behavior:
- States covered:
- Responsive behavior:
- Accessibility behavior:
- Migration risk:
- Why this should be system-wide:
```

### New Component Creation

Create a new component only when:

- no existing primitive fits the job
- adapting an existing component would create confusing variants
- the interaction pattern is genuinely new
- the information structure needs a new reusable pattern
- the product would benefit from standardizing the new pattern

When creating a new component, define:

- purpose
- anatomy
- props or content slots
- variants
- states
- responsive behavior
- accessibility behavior
- usage rules
- anti-patterns

Use this format when useful:

```text
New component:
- Name:
- Purpose:
- Anatomy:
- Variants:
- States:
- Responsive behavior:
- Accessibility behavior:
- When to use:
- When not to use:
```

### Anti-Patterns

Avoid:

- styling one instance when the primitive is broken
- creating many one-off classes for repeated problems
- changing shared components without checking usage
- adding new tokens for every screen
- mixing multiple visual systems
- using UI kit defaults unchanged
- adding decorative variants without hierarchy
- relying on color alone for state
- shipping components without focus, disabled, loading, and error behavior
- preserving component structure when the pattern is wrong
- making everything consistent by making everything visually flat

The system should make good design easier to repeat.
