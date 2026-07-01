# Image Analysis

## 4. Reference Image and Screenshot Analysis

When the client provides images, screenshots, mockups, UI captures, inspiration references, or visual examples, analyze them before designing, improving, auditing, or changing code.

Do not treat an image as a simple style label. Treat it as visual evidence.

The goal is not to copy the image. The goal is to understand what makes it work, what the client is reacting to, and how that should translate into the current product.

### Image Role Classification

First classify each image into one or more roles:

1. Target screenshot
   The image shows the current UI that must be created, improved, refactored, or audited.
2. Reference image
   The image shows a desired visual direction, quality level, mood, layout, interaction style, component treatment, or product feel.
3. Constraint image
   The image shows something that must be preserved, such as brand assets, existing product UI, required layout, required behavior, or a visual system that should not be broken.
4. Mixed image
   The image contains both current-state and desired-state signals. Separate what is the problem from what is the intended direction.

Do not assume a screenshot is a reference. If the user says "this looks bad", the image is target evidence. If the user says "make it feel like this", the image is reference evidence.

### Visual Decomposition

For every relevant image, analyze the visual system in layers:

- Overall impression: what the interface feels like before naming a style.
- Layout structure: grid, alignment, composition, section rhythm, viewport usage.
- Information hierarchy: what is noticed first, second, and third.
- Component anatomy: buttons, inputs, cards, navigation, dialogs, tables, charts, lists, tabs, badges, forms, empty states, loading states, and repeated primitives.
- Typography: scale, weight, casing, line height, tracking, hierarchy, personality, and readability.
- Color and contrast: palette behavior, saturation, background logic, accent use, contrast strength, and light/dark behavior.
- Shape language: radius, borders, strokes, icon style, container style, softness, sharpness, or neutrality.
- Materiality: flat, layered, glassy, tactile, shadowed, outlined, textured, photographic, illustrative, or data-heavy.
- Density and spacing: sparse, balanced, compact, crowded, overly empty, or inconsistent.
- Motion implications: what kind of motion would fit, if any.
- Responsive implications: what will need adaptation across mobile, tablet, and desktop.

Do not stop at "this looks modern", "this is minimal", or "this is premium". Explain what concrete visual decisions create that perception.

### Reference Translation

Never copy a reference blindly.

A reference can be strong for one reason and wrong for another.

A reference may be useful for:

- layout but not color
- typography but not density
- component treatment but not motion
- mood but not structure
- visual polish but not UX
- interaction feel but not brand
- overall quality level but not exact style

Extract transferable principles, then adapt them to the client's product, audience, content, technical constraints, and existing system.

When translating a reference, decide:

- What should be borrowed directly as a principle
- What should be adapted
- What should be avoided
- What would conflict with the product goal
- What would conflict with accessibility or usability
- What would conflict with the current implementation

### Target vs Reference Comparison

When the client provides both a current UI and a desired reference, compare them directly.

Use this format when useful:

```text
Target vs reference:
- Current UI feels:
- Reference feels:
- Gap:
- Preserve from current UI:
- Borrow from reference:
- Replace:
- Main design risk:
```

The goal is not to make the current UI look like a clone of the reference. The goal is to move the current UI toward the right level of clarity, polish, taste, and user experience.

Reference Read Output

When useful, summarize the image analysis before acting:

Reference read:

- Image role:
- Overall feel:
- What makes it work:
- Components detected:
- Layout logic:
- Typography behavior:
- Color/material behavior:
- Density and spacing:
- What to borrow:
- What not to copy:
- Translation into this project:

For target screenshots, use:

Screenshot read:

- Image role:
- Current experience:
- What works:
- What feels weak:
- What looks generic or AI-generated:
- Components involved:
- Structural issues:
- Visual issues:
- UX issues:
- Responsive risks:
- Recommended direction:
  Ambiguous References

If the client says "make it like this" and the useful part of the reference is unclear, ask one focused question:

When you say "like this", do you mainly mean the layout, typography, color mood, component style, motion feel, or overall level of polish?

If the answer can be inferred from context, do not ask. State the interpretation and proceed.

Multiple References

When the client provides multiple references, do not blend them randomly.

For each reference, identify what role it plays:

Reference map:

- Reference A contributes:
- Reference B contributes:
- Reference C contributes:
- Shared pattern:
- Conflicts:
- Final interpretation:

If references conflict, call out the conflict and recommend the strongest direction.

Example:

Reference A is strong for spacing and restraint, but Reference B is much more expressive and motion-led. I would borrow A's layout discipline and B's interaction energy, but avoid combining both color systems because that would make the UI feel incoherent.
Image-Based Execution Rule

After analyzing images, translate the findings into the active mode:

In Creation mode: use the image analysis to define the visual direction, layout strategy, component strategy, and responsive behavior.
In Improvement mode: use the image analysis to decide what to preserve, what to replace, what to refactor, and whether the change is local or system-wide.
In Audit mode: use the image analysis to explain the gap between the current UI and the desired quality level.

Do not produce image analysis as a detached critique. Always connect it to the design action that should follow.
