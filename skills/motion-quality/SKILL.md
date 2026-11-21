---
name: motion-quality
description: "Decide whether and how to animate: purpose, properties, duration, easing, interruption, reduced motion, and performance. Use when adding transitions, micro-interactions, page or route changes, drag and gesture motion, loading states, or when animation feels gratuitous, sluggish, or janky. Produces motion that clarifies cause and effect instead of decorating the interface."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: design
  standard: agentskills.io
---

# Motion Quality

Motion is a functional layer: it explains where something came from, what changed, and what
the user can do next. If it does not answer one of those questions, it is decoration — and
decoration has a cost in attention, performance, and accessibility.

## Decision gate: should it animate?

Animate only when at least one is true:

- **Continuity:** an element moves between two states/places and the user needs to track it.
- **Cause and effect:** a user action produces a visible result that could otherwise be missed.
- **Hierarchy:** an overlay/panel enters with a spatial relationship to its trigger.
- **Feedback:** a press, toggle, or drop needs immediate confirmation.
- **Progress:** work takes long enough that the user needs to know it is happening.

Do **not** animate:

- Content appearing on page load just to stagger it.
- Every hover, card, and icon with the same lift.
- Route changes for spectacle.
- Anything that delays the user's next action.
- Decorative loops, parallax, or autoplay that cannot be paused.
- A state change where an instant swap is clearer (e.g., a checkbox).

## Core parameters

| Interaction | Duration | Easing |
| --- | --- | --- |
| Press/tap feedback | 80–120 ms | ease-out |
| Hover/color/border | 120–180 ms | ease-out |
| Tooltip/popover enter | 120–180 ms | ease-out (decelerate) |
| Popover exit | 80–120 ms | ease-in (accelerate) |
| Modal/sheet enter | 200–300 ms | ease-out or spring |
| Modal/sheet exit | 150–200 ms | ease-in |
| Page/route transition | 200–350 ms | ease-in-out |
| List reorder / layout | 200–300 ms | spring or ease-out |
| Drag release / momentum | spring | critically damped or slight overshoot |

Rules:

- Exit is faster than enter; the user has already decided.
- Distance matters: longer travel can take slightly longer, but cap around 400 ms.
- Small elements move faster than large surfaces.
- Use a spring only when physical continuity matters (drag, sheet, reorder). For simple
  fades/color, a cubic-bezier is cheaper and more predictable.
- Standardize on 2–3 durations and 2–3 easings in tokens; do not tune every component.

## Properties

Animate **transform** and **opacity** by default. They can run on the compositor.

Avoid animating layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`) on
anything that runs during interaction; they trigger layout and paint. If a size change is
required, use `transform: scale` carefully (it distorts children) or animate a wrapper's
grid track where supported. Animate `filter`/`box-shadow` sparingly; they are expensive.

Never animate:

- `display` (use enter/exit with `@starting-style` or a JS presence state).
- Color of large surfaces at high frequency.
- `height: auto` in a loop; measure and animate a fixed max-height/grid track instead.
- Background images or large blurs on low-end devices.

## Interruption and continuity

- Motion must be interruptible. If the user reverses a gesture or closes a panel mid-open,
  the animation should follow the new intent, not finish the old one.
- Use a spring or a velocity-aware transition for gestures; do not restart from zero.
- Preserve spatial continuity: a modal grows from its trigger, a sheet slides from the edge
  it belongs to, a deleted row collapses where it was.
- Route transitions should preserve the sense of place: shared elements move, unrelated
  content cross-fades or swaps.
- Never block input until an animation finishes. The UI should respond immediately; motion
  is feedback, not a gate.

## Accessibility

- Honor `prefers-reduced-motion: reduce`: remove transforms, parallax, and large movement;
  keep opacity/instant state changes. Do not remove all feedback, just the motion.
- No flashing more than three times per second.
- No autoplay with sound; provide pause/stop for auto-moving content.
- Motion that conveys meaning needs a non-motion equivalent (e.g., a status text).
- Focus indicators must not be animated away or obscured.
- Avoid motion that triggers vestibular symptoms: large zoom, spin, bounce, parallax.
- Keep animation durations short enough that cognitive/attention differences are not punished.

## Performance

- Test on a mid-range phone, not only a desktop.
- Watch long tasks, dropped frames, and layout shifts during the animation.
- Animate only compositor-friendly properties; avoid per-frame layout reads.
- Use `will-change` sparingly and remove it after the animation.
- Do not animate a large blurred surface or a giant SVG path on every frame.
- Batch DOM reads/writes; use `requestAnimationFrame` or the platform's animation API.
- Respect the device: reduce or disable heavy motion on low-power mode where possible.

## Choreography

- **One thing at a time.** A single clear transition beats five simultaneous effects.
- **Stagger only for related items** entering together, with a small offset (20–40 ms), not
  a cascade that makes the user wait.
- **Shared element** transitions are for continuity, not for showing off.
- **Exit before enter** when replacing content in the same space; overlap only when the
  relationship is clear.
- **Sound/haptics** are separate feedback channels; do not use them to compensate for weak
  visual feedback.

## Review checklist

For an existing animation, ask:

- What question does this motion answer? If none, remove it.
- Does it delay the user's next action? If yes, shorten or remove.
- Does it animate layout or paint on every frame? If yes, change the property.
- Can it be interrupted? What happens if the user reverses mid-animation?
- Does it respect reduced motion? Is the fallback still informative?
- Is the duration/easing consistent with the rest of the product?
- Does it work on a slow device and a large screen?
- Is the spatial origin correct (where did it come from)?
- Does it compete with another animation on the same screen?

## Gotchas

- **`transition: all`** animates properties you did not intend, including layout. List
  properties explicitly.
- **Enter animations on first paint** can look like a flash or delay content. Use them for
  state changes, not initial render.
- **Exit animations need presence state.** Removing an element from the DOM immediately makes
  the exit impossible; keep it mounted until the animation completes.
- **Height animations** are a common jank source. Use grid-template-rows, max-height with a
  measured value, or a layout animation library.
- **Springs can overshoot** and clip content; tune damping and test at the edges.
- **Reduced motion is not "no feedback".** Keep the state change, drop the movement.
- **Dark mode/low-end devices** may reveal compositing artifacts; test both.
- **Animation libraries add bundle weight.** Use the platform (CSS/WAAPI) unless the
  interaction genuinely needs orchestration.

## Output contract

```markdown
## Purpose
[Which gate: continuity / cause-effect / hierarchy / feedback / progress.]

## Motion spec
| Element | Trigger | Property | Duration | Easing | Reduced motion |
| --- | --- | --- | --- | --- | --- |

## Interruption
[Gesture reversal, rapid toggles, route change mid-animation.]

## Performance
[Properties used, device tested, frame/long-task check.]

## Removed
[Animations considered and rejected because they added no information.]
```

## Quality gate

- [ ] Every animation answers a continuity/cause-effect/hierarchy/feedback/progress question.
- [ ] Durations follow the scale; exits are faster than enters.
- [ ] Only transform/opacity (or another compositor-friendly property) animate during
      interaction.
- [ ] Motion is interruptible and follows the user's latest intent.
- [ ] Reduced motion is honored and still communicates the state change.
- [ ] No autoplay/flashing/vestibular hazards.
- [ ] Tested on a mid-range device; no dropped-frame jank.
- [ ] Decorative animation was removed, not just toned down.
