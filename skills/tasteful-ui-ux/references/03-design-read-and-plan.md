# Design Read And Plan

## 5. Design Read and Execution Plan

Before creating, improving, or auditing, synthesize the evidence into a clear design read.

Do not jump from brief to output.

The design read is the moment where you convert evidence, references, client taste, constraints, and UX problems into an intentional direction.

Keep it concise. The design read should guide execution, not become a long essay.

### When to Produce a Design Read

Produce a design read when:

- the request involves a full page, screen, flow, component system, or visual direction
- the user provides screenshots or references
- the user asks for something vague like "make it beautiful", "modern", "impactful", "premium", or "less generic"
- the UI is being improved or audited
- there is a risk of changing functionality, structure, or system-wide primitives

For very small, obvious fixes, use a shorter read or proceed directly.

### Design Read Format

Use this format when useful:

```text
Design read:
- Mode:
- Scope:
- Client clarity level:
- Current state:
- Desired outcome:
- Visual direction:
- Main UX/design risk:
- Preserve:
- Change:
- Execution approach:
```

Do not fill fields mechanically. Include only what helps the work.

### Client Intent Checkpoint

When the user asks to improve a real product, real SaaS, production landing page, or existing business-facing interface with a vague goal such as "make it impressive", "make it beautiful", "make it less generic", "make it more premium", or "make it convert better", do not jump directly into redesign.

First inspect the evidence.

Then decide whether the missing information would materially change the direction.

Ask 1-5 high-leverage questions only when the missing answers would affect positioning, visual direction, conversion strategy, brand preservation, proof strategy, or content hierarchy.

Do not ask generic design questions. Ask questions the client can answer.

#### When Questions Are Required

Ask questions before redesigning when:

- the product is real and business-facing, not a fixture or experiment
- the user asks for a vague quality improvement
- the target audience is unclear
- the primary conversion goal is unclear
- the current brand should maybe be preserved but this is not stated
- the user has not said what should not change
- there are no references or competitors
- the requested direction could lead to multiple valid redesign paths

#### When Questions Are Not Required

Do not block execution when:

- the user explicitly says to proceed without questions
- the task is a small local fix
- the brief includes enough product, audience, goal, constraints, and reference evidence
- the user asks for an audit only
- the work is clearly experimental or a test fixture

#### Question Style

Ask questions in the user's language.

Ask no more than 5 questions.

Prefer questions about intent, audience, conversion, trust, and constraints.

Avoid questions like:

- What typography do you want?
- What color palette do you want?
- What design style do you want?
- Should it be minimal or brutalist?

Prefer questions like:

- Who is the landing mainly trying to convince?
- What is the main action you want visitors to take?
- What must stay recognizable from the current brand?
- What feels most wrong today: trust, clarity, polish, conversion, or differentiation?
- Are there competitors or references you want to move closer to or away from?

#### Client Intent Output

Use this format before asking:

```text
Client intent checkpoint:
- I can infer:
- I cannot safely infer:
- Why it matters:
- Questions:
```

If the user answers, use the answers as direction.

If the user does not answer and asks you to proceed, state assumptions and continue.

### Mode-Specific Execution Plans

After the design read, choose the execution plan based on the active mode.

#### Creation Mode

Use when creating a new interface, screen, page, flow, component, design direction, or responsive web experience.

Execution plan should define:

what is being created
target user or audience, if known
primary user action or experience
visual direction
layout strategy
component strategy
content hierarchy
responsive behavior
interaction and motion approach
implementation constraints

Use this format when useful:

Creation plan:

- Interface:
- Primary goal:
- User/audience:
- Visual direction:
- Layout strategy:
- Component strategy:
- Responsive strategy:
- Motion/interaction strategy:
- Implementation notes:

#### Improvement Mode

Use when improving an existing UI, screenshot, component, flow, or project.

Execution plan should define:

what is weak today
what should be preserved
what should change
intervention level
whether the fix is local or system-wide
how the change improves UX, hierarchy, responsiveness, or product feel

Use this format when useful:

Improvement plan:

- Current problem:
- Intervention level:
- Preserve:
- Change:
- Local or system-wide:
- UX improvement:
- Visual improvement:
- Implementation notes:

#### Audit Mode

Use when reviewing or diagnosing a UI without immediately redesigning it.

Execution plan should define:

what is working
what is weak
what is broken
what is generic or AI-looking
what is highest priority
recommended fixes
severity and order of operations

Use this format when useful:

Audit plan:

- What works:
- Critical issues:
- Important issues:
- Refinement issues:
- Responsive risks:
- Accessibility risks:
- AI-looking patterns:
- Recommended order:

### Assumptions and Missing Information

If important information is missing, do not invent silently.

Either ask the minimum necessary question or proceed with stated assumptions.

Use this format:

Assumptions:

- I will assume:
- I will not assume:
- Risk:

Ask a question only when the answer would materially change the design direction or implementation.
If the user explicitly invited questions, treat that as permission to ask the minimum focused question when ambiguity remains material.

Do not ask questions to avoid making judgment.

### Proceeding Without Approval

Do not require approval after every design read.

Proceed when:

the brief is clear enough
the missing details do not materially change the solution
the user asked for execution
the best direction can be reasonably inferred

Ask before proceeding when:

the user gave conflicting visual directions
the change may alter functionality or user flow
a local change may need to become system-wide
the reference image can be interpreted in several incompatible ways
brand, accessibility, or implementation constraints are unclear
the user asked for execution but also explicitly invited questions, and the product positioning, target audience, or taste target is still materially ambiguous after evidence review

### Design Read Examples

Example for vague improvement:

Design read:

- Mode: Improvement
- Scope: existing app UI
- Client clarity level: no clear direction
- Current state: the interface feels generic because hierarchy, spacing, and component treatment appear template-driven
- Desired outcome: make the app feel more intentional, trustworthy, and product-specific
- Visual direction: calmer structure, stronger hierarchy, less decorative noise, more system consistency
- Main UX/design risk: only adding visual effects without fixing the underlying experience
- Preserve: existing functionality, data, navigation, and user flow
- Change: layout rhythm, component hierarchy, spacing, visual language, interaction states
- Execution approach: diagnose the repeated patterns first, then refactor the highest-impact surfaces

Example for reference-led improvement:

Design read:

- Mode: Improvement
- Scope: current screen using reference image as direction
- Client clarity level: reference-led
- Current state: the current UI lacks the polish and hierarchy shown in the reference
- Desired outcome: move toward the reference's quality level without cloning it
- Visual direction: borrow the reference's spacing discipline, component restraint, and stronger visual hierarchy
- Main UX/design risk: copying colors or decoration without translating the underlying structure
- Preserve: product behavior, existing content, and required components
- Change: composition, typography scale, density, component treatment, and responsive behavior
- Execution approach: compare target vs reference, extract transferable principles, then apply them to the current UI

Example for primitive component work:

Design read:

- Mode: Improvement
- Scope: button primitive
- Client clarity level: vague direction
- Current state: the button feels default and does not carry the product's visual language
- Desired outcome: create a reusable button system that feels intentional across the app
- Visual direction: clearer hierarchy between primary, secondary, destructive, ghost, disabled, loading, hover, active, and focus states
- Main UX/design risk: styling only one instance while the system remains inconsistent
- Preserve: component API, accessibility, keyboard behavior, loading behavior
- Change: visual states, spacing, typography, radius, contrast, and motion feedback
- Execution approach: treat this as a system-level primitive unless the user says the change is local
