# Final Quality Gate

Use this before final delivery, after audits, and after major redesigns.

The goal is not only to make the interface prettier. The goal is to ensure the result is specific, honest, usable, responsive, and not merely a different AI-looking template.

## 1. Cliché Substitution Check

Do not replace one generic pattern with another.

Common substitutions that still fail:

- dark SaaS with purple glow -> warm editorial beige SaaS
- AI gradient hero -> serif manifesto hero
- fake workflow diagram -> fake terminal/log card
- three feature cards -> numbered feature list with the same generic content
- vague metrics cards -> inline fake proof strip
- generic testimonial card -> fake quote with placeholder avatar
- decorative glassmorphism -> decorative paper/editorial styling
- centered hero -> asymmetric hero with no stronger concept

Ask:

- Did the redesign become more specific, or just switch templates?
- Would this visual direction fit ten unrelated startups?
- Is the concept shaping the interface, or only the copy?
- Are the visual decisions inevitable for this product?
- Did we remove the original weakness, or disguise it?

If the answer is weak, do not ship. Redesign the underlying idea.

## 2. Fake Proof Check

Do not present invented proof as real.

Flag:

- fake metrics
- fake testimonials
- fake ratings
- fake customer counts
- fake logs
- fake “live” indicators
- fake product screenshots
- fake terminal output
- fake avatars
- fake company names
- fake security/compliance claims

Allowed:

- clearly marked mock/example content
- realistic placeholder content that is not presented as proof
- product UI examples that are clearly illustrative
- real user-provided data
- real references from the product or docs

If proof is not real, either remove it, label it as illustrative, or replace it with a more honest content pattern.

## 3. Concept Depth Check

A strong concept must affect structure, not only language.

Ask:

- Does the product idea change the layout?
- Does it change the interaction model?
- Does it change the hierarchy?
- Does it change the component choices?
- Does it change what is shown first?
- Does it change how proof is presented?
- Does it create a memorable product-specific pattern?

If the concept only appears in headline wordplay, footer copy, badges, or section labels, it is not deep enough.

## 4. Copy Authenticity Check

Flag copy that sounds like AI trying to be clever.

Watch for:

- aphorisms that reduce clarity
- over-crafted headlines
- fake humility
- forced metaphors
- “real” claims attached to fake content
- generic verbs such as ship, scale, unlock, elevate, streamline, accelerate
- poetic labels that do not help comprehension
- invented quotes that sound like marketing copy

Prefer copy that is specific, plain, and useful.

Good copy can be memorable, but it must still explain the product.

## 5. Visual Direction Check

A visual direction is weak if it depends on familiar trend bundles.

Flag overused bundles:

- dark background + purple accent + grid + glow
- cream paper + terracotta + serif + mono
- glass panels + gradients + blur
- giant centered headline + three equal cards
- terminal mockup + fake log lines
- bento grid with generic feature claims
- numbered feature rows with no real product specificity

A direction is stronger when:

- it emerges from the product's job
- it supports the user's task
- it creates a recognizable product rhythm
- it can be explained without naming a trend
- it makes the interface clearer, not just prettier

## 6. Responsive and System Check

Before shipping, verify:

- mobile hierarchy is not a compressed desktop layout
- CTAs remain reachable
- navigation remains usable
- cards, forms, tables, charts, and overlays adapt intentionally
- shared primitives remain consistent
- accessibility is preserved
- interaction states are present
- the system does not gain random one-off styling

## 7. Final Readiness Output

Before final delivery, use this format when useful:

```text
Quality gate:
- Cliché substitution risk:
- Fake proof risk:
- Concept depth:
- Copy authenticity:
- Visual specificity:
- Responsive readiness:
- System consistency:
- Must fix before shipping:
```

If there are must-fix issues, fix them before claiming the work is complete.

## If a Cliché Is Detected, Change the Source Pattern

When the quality gate identifies cliché substitution, do not only rename labels or remove fake proof.

Change the source pattern that created the cliché.

Examples:
- If warm editorial SaaS is detected, reconsider palette, type system, layout rhythm, and content framing.
- If fake terminal visuals are detected, replace them with real product logic, a decision timeline, annotated state flow, or honest illustrative content.
- If the headline is clever but unclear, prioritize product comprehension over wordplay.
- If the concept is strongest in a lower section, consider moving that structure into the hero.