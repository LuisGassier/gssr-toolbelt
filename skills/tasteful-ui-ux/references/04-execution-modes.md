# Execution Modes

## 6. Execution Rules by Mode

After the design read, execute according to the active mode.

Do not use the same workflow for creation, improvement, and audit. Each mode has a different responsibility.

The three modes are:

- Creation: produce a new interface, screen, flow, component, system direction, or responsive experience.
- Improvement: change an existing UI without breaking what must keep working.
- Audit: diagnose quality, UX, responsiveness, accessibility, and visual issues before proposing fixes.

Always connect execution to the client’s goal, evidence, references, constraints, and design read.

---

### 6.1 Creation Mode

Use Creation Mode when the client asks for something new.

Examples:

- "Create a landing page"
- "Design this dashboard screen"
- "Build a pricing page"
- "Create a button system"
- "Design the empty states"
- "Make a new onboarding flow"
- "Create a responsive app layout"

Creation Mode is not decoration. It is product design and interface direction.

Before creating, define:

- What is being created
- What user or audience it serves
- What the primary action or experience is
- What content or data must be represented
- What visual direction fits the goal
- What layout strategy supports the hierarchy
- What components or patterns are needed
- What responsive behavior is required
- What interaction states must exist
- What implementation constraints apply

When creating, produce the strongest appropriate solution, not the most obvious UI kit composition.

Do not default to:

- centered hero plus three cards
- generic dashboard cards
- random gradients
- decorative glass panels
- oversized headings without hierarchy
- equal-width sections everywhere
- UI kit defaults without adaptation

Instead, define the experience from the user’s task and desired perception.

#### Creation Checklist

Before delivering Creation Mode output, verify:

- The interface has a clear purpose.
- The first screen communicates the main idea quickly.
- The hierarchy tells the user what matters first.
- The layout supports the content instead of forcing content into a template.
- The component choices match the user task.
- The design direction is specific to this product.
- The responsive behavior is explicit.
- Important states are included: loading, empty, error, disabled, hover, active, focus, selected when relevant.
- The output can be implemented with the current stack or with clearly stated assumptions.

#### Creation Output

Use this format when useful:

```text
Creation output:
- Interface created:
- Design direction:
- Main structure:
- Key components:
- Responsive behavior:
- Interaction states:
- Implementation notes:
- Why this works:
```

---

### 6.2 Improvement Mode

Use Improvement Mode when the client provides an existing UI, screenshot, code, flow, primitive, or project and wants it changed.

Examples:

- "Make this look better"
- "This looks AI-generated"
- "Improve this dashboard"
- "This card feels generic"
- "Modernize these screens"
- "Refactor this button"
- "Make the app more beautiful"
- "Use this reference to improve my current UI"

Improvement Mode starts with diagnosis.

Do not jump directly to styling changes.

First determine:

- What is weak in the current experience
- What should be preserved
- What should change
- Whether the issue is visual, structural, informational, interactive, responsive, or systemic
- Whether the change is local or system-wide
- Whether the current UI pattern is the right pattern
- Whether the client’s requested change would actually solve the problem

Improvement may require:

- surface refinement
- structural refinement
- pattern replacement
- flow-level change
- system-level change
- content and hierarchy change
- net-new design direction

Do not preserve the existing UI shape if the shape is the problem.

#### Improvement Priorities

Apply improvements in this order:

1. Preserve what must not break.
2. Clarify the user goal and hierarchy.
3. Fix the structure or pattern if needed.
4. Improve layout, spacing, and density.
5. Improve typography and content hierarchy.
6. Improve color, contrast, material, and shape language.
7. Improve states and interaction feedback.
8. Improve responsive behavior.
9. Add motion only when it supports the experience.
10. Remove AI-looking or generic patterns.

Cosmetic changes are acceptable only after the experience is structurally sound.

#### Improvement Output

Use this format when useful:

```text
Improvement output:
- Current issue:
- Intervention level:
- Preserve:
- Change:
- Local or system-wide:
- UX improvement:
- Visual improvement:
- Responsive improvement:
- Implementation notes:
```

When giving code changes, explain the design reason behind major changes.

Do not only say what changed. Explain why it improves the interface.

---

### 6.3 Audit Mode

Use Audit Mode when the client asks for critique, review, diagnosis, responsive analysis, UX analysis, accessibility review, or visual quality review.

Examples:

- "Audit this UI"
- "What is wrong with this design?"
- "Why does this look generic?"
- "Review this page on mobile"
- "Tell me why this does not feel premium"
- "Find UX problems"
- "Check if this is responsive"
- "What should I improve first?"

Audit Mode should diagnose before redesigning.

Do not immediately rewrite the UI unless the client asks for fixes.

Audit the interface across:

- UX clarity
- information hierarchy
- visual hierarchy
- layout structure
- component choice
- content density
- typography
- color and contrast
- spacing and rhythm
- responsive behavior
- accessibility
- interaction states
- motion quality
- consistency
- AI-looking patterns
- implementation risk

Prioritize findings by severity.

#### Audit Severity Levels

Use these levels:

1. Critical
   Breaks usability, accessibility, responsiveness, comprehension, task completion, or functionality.
2. Important
   Weakens clarity, hierarchy, trust, polish, conversion, or system consistency.
3. Refinement
   Improves craft, visual taste, perceived quality, or interaction feel but does not block the experience.

#### Audit Output

Use this format when useful:

```text
Audit output:
- Overall read:
- What works:
- Critical issues:
- Important issues:
- Refinements:
- AI-looking patterns:
- Responsive risks:
- Accessibility risks:
- Recommended order of fixes:
```

For code or component audits, use a table when comparing current vs recommended changes:

```text
| Current | Recommended | Why |
| --- | --- | --- |
| ... | ... | ... |
```

Do not produce vague critique like "improve spacing" or "make it more modern".

Every audit finding must be actionable.

Bad:

- "The page needs better hierarchy."

Good:

- "The primary CTA competes with three secondary actions in the hero. Make one primary action visually dominant, move secondary actions below the main copy, and reduce button variants to one primary plus one secondary."

---

### 6.4 Mode Switching

A request may start in one mode and move into another.

Examples:

- Audit → Improvement
  The client asks what is wrong, then asks you to fix it.
- Improvement → System-level Improvement
  A local button issue reveals a broken button primitive used across the app.
- Creation → Audit
  After creating a draft, review it against the design read before finalizing.
- Reference Analysis → Improvement
  The client provides a reference, then asks to apply it to an existing UI.

Switch modes when the work requires it, but state the switch briefly.

Example:

```text
This started as a local visual improvement, but the issue is coming from the shared card primitive. I will treat this as a system-level improvement so the fix applies consistently.
```

---

### 6.5 Execution Discipline

During execution:

- Do not ask unnecessary questions.
- Do not avoid judgment.
- Do not make the client solve design decisions alone.
- Do not apply visual trends without purpose.
- Do not preserve broken structure.
- Do not make cosmetic-only changes when the experience needs structural work.
- Do not overcomplicate simple interfaces.
- Do not introduce new dependencies unless they materially improve the result.
- Do not change functionality silently.
- Do not sacrifice accessibility for aesthetics.

Always prefer:

- clear hierarchy
- intentional layout
- strong responsive behavior
- system consistency
- useful interaction states
- readable typography
- disciplined spacing
- appropriate component choice
- product-specific visual language
- practical implementation

The final output should feel like a design decision, not a UI decoration pass.
