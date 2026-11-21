# Slop Pattern Catalog

Use as a diagnostic. Not every instance is slop; context decides. The replacement column is
a direction, not a drop-in phrase.

## Copy and marketing

| Pattern | Why it reads as slop | Replacement direction |
| --- | --- | --- |
| Seamless, effortless, robust, powerful, cutting-edge | Adjective with no behavior | The specific action and result |
| Unlock, unleash, elevate, supercharge, revolutionize | Hype verb | What the user can now do |
| In today's fast-paced world | Throat-clearing | Delete |
| It's worth noting / generally speaking | Hedge | State it or cut it |
| Leverage / utilize | Inflated verb | Use |
| Best-in-class / world-class / industry-leading | Unsupported ranking | A measured comparison or delete |
| Trusted by thousands | Unsupported social proof | Named customers with permission, or delete |
| 99.9% uptime | Unsupported number | Measured SLA with period and source |
| 10x faster | No baseline | "X ms → Y ms on [workload]" |
| AI-powered | Names the mechanism, not the value | The task it performs and the output |
| Take it to the next level | Empty | The next concrete step |
| Don't miss out / Act now | Manufactured urgency | The real deadline and consequence |
| Delve into / dive deep | Filler | Start with the point |
| Moreover / Furthermore / Additionally | Filler transition | Delete or use a plain link |
| In conclusion | Redundant | End with the decision or next step |
| Like, literally, just | Filler intensifier | Delete unless it carries meaning |

## Structure

- 12 sections for a 200-line README. Cut to what a reader needs: what, why, run, configure,
  limits.
- Three equal feature cards with icons and no hierarchy. Replace with the primary workflow
  and the evidence that it works.
- FAQ that answers questions nobody asked. Delete or answer real support questions.
- "Why choose us" with adjectives. Replace with a comparison or a concrete outcome.
- Testimonials with initials and no company. Either get permission and specifics, or remove.
- A hero with a gradient blob and a generic dashboard mockup. Show the real product or a
  task-specific composition.
- Emoji section headers (🚀 ✨ 🔥). Use plain headings; reserve emoji for human conversation.
- Every card rounded, shadowed, and hover-lifted. Pick one elevation language.
- Purple/indigo gradient + white card + Inter. A default, not a direction.

## Code

| Pattern | Problem | Better |
| --- | --- | --- |
| `utils.ts`, `helpers.py`, `common/` | Unrelated code with no owner | Name by domain: `money.ts`, `retry.ts` |
| `data`, `item`, `obj`, `manager`, `service` | Says nothing | Domain noun: `invoice`, `reservation` |
| `handleData`, `processItem`, `doWork` | Vague verb + vague noun | `reconcileInvoice`, `expireInvitations` |
| Interface with one implementation | Speculative abstraction | Concrete class/function until a second use |
| Factory + registry for two types | Ceremony | A switch or map at the call site |
| Wrapper that forwards all args | Indirection with no value | Call the underlying API |
| `try { ... } catch (e) {}` | Swallows failure | Handle, rethrow, or remove the catch |
| `// increment i` | Restates code | Delete; comment the invariant instead |
| JSDoc on every trivial function | Noise | Document non-obvious contracts and units |
| `TODO: implement` in shipped code | Broken promise | Implement, remove, or file a tracked issue |
| `@ts-ignore`, `any`, `# type: ignore` | Silenced safety | Fix the type or isolate with a comment |
| Commented-out code | Dead weight | Delete; git remembers |
| `sleep(1000)` in tests | Flaky | Await the condition |
| `localhost` / `example.com` in config | Environment leak | Env var with a safe default |
| Placeholder API keys committed | Secret risk | Remove and rotate |

## UI and visual

- Generic gradient hero with a floating card and no product-specific content.
- Three identical stat cards with invented numbers.
- Icon + title + two-line description repeated six times.
- Glassmorphism applied to every surface regardless of depth.
- Neon glow on primary actions in a serious B2B tool.
- Excessive border radius and shadows to compensate for weak hierarchy.
- Lorem ipsum or "Your text here" in a deliverable.
- Fake user avatars from a random face generator presented as customers.
- Charts with no axis labels, units, or time range.
- Empty states that say "No data" with no next action.
- Dark mode implemented as an inverted afterthought with unreadable contrast.
- Animation on everything, including page load, hover, scroll, and route change.

## Docs and READMEs

- Opening with "Welcome to [project]!" and a paragraph about the project's journey.
- A feature list that is really a table of contents.
- Install instructions that assume the author's machine.
- No mention of prerequisites, versions, or known limitations.
- Screenshots that are outdated or show fake data without a label.
- "Contributing" copied from a template with no project-specific steps.
- Badges for CI that does not exist.
- A license section that contradicts the LICENSE file.
- Examples that cannot be run as written.

## Tests

- `test1`, `works`, `should work`, `test_create`.
- Asserting a mock was called instead of the behavior that matters.
- Snapshot tests with no reviewed baseline.
- Coverage padding: trivial getters and framework behavior.
- Sleeping or retrying to hide a race.
- One giant test that fails without a useful message.
- Fixtures with `foo`, `bar`, `John Doe` where the domain matters.

## PRs and commit messages

- "Fix stuff", "WIP", "Update code", "Address comments".
- A description that restates the diff instead of the why.
- No test plan, no risk, no rollback.
- Mixing refactor, feature, and formatting in one change.
- Screenshots with no before/after or context.
- "Tested manually" with no steps.

## The replacement test

For any sentence, ask:

1. Is it true? (Can I source it?)
2. Is it specific? (Does it name a who, what, when, or number?)
3. Is it useful? (Would the reader do something differently?)
4. Is it the simplest way to say it?

If the answer is no to 1–3, delete it. If yes to all four, keep it even if it uses a word
from this catalog.
