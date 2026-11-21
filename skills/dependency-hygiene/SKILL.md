---
name: dependency-hygiene
description: "Decide whether to add a dependency, keep it healthy, or remove it: build-vs-buy, maintenance signals, security, license, bundle/runtime cost, pinning, update cadence, and unused packages. Use when installing a package, reviewing package.json or requirements, shrinking a bundle or image, responding to an advisory, or cleaning up a stale dependency tree. Treats every dependency as code you now maintain."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: engineering-craft
  standard: agentskills.io
---

# Dependency Hygiene

A dependency is code you ship, deploy, patch, and defend — but did not write. The question is
never "does it save lines today?" It is "is this cheaper than owning the functionality for the
life of the product?"

Default stance: **use the platform, write the small thing, and add a dependency only when it
is clearly cheaper to adopt than to own.**

## Non-negotiables

1. **Every dependency needs a reason** that survives the demo: capability, reliability, or
   cost that would take significant effort to match.
2. **Check the transitive tree**, not just the package you name. One install can add dozens.
3. **Check maintenance, security, license, and size** before adding, not after the incident.
4. **Pin and lock.** Reproducible installs; review lockfile changes.
5. **Remove unused dependencies.** They are attack surface and install time with no value.
6. **Do not add a package for a one-liner** the standard library or platform already provides.

## Decision: add, build, or use the platform

| Need | Prefer |
| --- | --- |
| Date/number formatting, i18n | Platform `Intl` |
| HTTP requests | Platform `fetch` / stdlib |
| UUID, slug, base64, hashing (non-crypto) | Platform/stdlib |
| Simple validation | Schema/type system or a few lines |
| One utility function | Write it, test it |
| Complex domain protocol (payments, auth, parsing) | Vetted library or vendor |
| UI primitives with accessibility | Established headless library or design system |
| Infrastructure glue | Official SDK/client |

Add a dependency when at least two are true:

- The functionality is non-trivial and easy to get wrong (crypto, time zones, parsers,
  protocols).
- The package is actively maintained and widely used.
- The security/license/size profile is acceptable.
- Owning it would cost more than adopting it over the expected lifetime.
- It composes with the existing stack without a parallel runtime or build system.

Do not add when:

- A platform API or stdlib covers it.
- It is a thin wrapper around something you already have.
- It pulls a large tree for one function.
- It is abandoned, unmaintained, or has unresolved critical advisories.
- The license conflicts with distribution or commercial use.
- You cannot explain what it does at the boundary.

## Evaluation checklist

Before adding:

- [ ] **Function:** does it actually solve the problem, including edge cases you need?
- [ ] **Maintenance:** recent releases, responsive issues, bus factor, clear ownership.
- [ ] **Security:** advisories, install scripts, provenance, 2FA/publishing posture.
- [ ] **Size:** install size and runtime/bundle cost for the parts you use.
- [ ] **License:** compatible with the product's distribution and business model.
- [ ] **API stability:** semver discipline, migration burden, TypeScript/types quality.
- [ ] **Transitive tree:** how many packages, duplicates, native builds, postinstall scripts?
- [ ] **Exit cost:** can you wrap it behind a small adapter and replace it later?
- [ ] **Alternatives:** platform, existing dependency, smaller package, or write it.

Record the reason in the PR. "Needed for X" is enough; a paragraph is better for a large or
unusual dependency.

## Adding safely

1. Install with the lockfile update; review the full lockfile diff, not just the manifest.
2. Read the package's install scripts; disable them in CI if not needed.
3. Import only the submodule/function you need where the package supports it.
4. Wrap third-party APIs behind a small adapter when the surface is broad or likely to change.
5. Add a test at the integration boundary, not just a unit test with a mock.
6. Run the audit and the build; check bundle/image size.
7. Document the reason and any operational implications (credentials, rate limits, data
   residency).

## Updating

- Set a cadence (weekly/monthly) and automate the boring part (Dependabot/Renovate).
- Read the changelog for minor/major updates; do not merge blindly because CI is green.
- Treat major updates as migrations: read the breaking changes, update code, test, canary.
- Keep security patches fast-tracked; do not let a critical advisory wait for the monthly train.
- Watch for duplicate versions of the same package; dedupe or align ranges.
- Re-check licenses after upgrades; they can change.

## Removing

Find unused packages:

```bash
# JavaScript
npx depcheck
npm ls --all
npx source-map-explorer dist/assets/*.js

# Python
pipdeptree
python -m pip list --not-required

# Go
go mod why ./...
go mod tidy

# Rust
cargo machete
cargo tree
```

Then:

1. Remove the import and the manifest entry.
2. Regenerate the lockfile.
3. Run tests/build; check the bundle/image size.
4. Replace with the platform or a local function when the package was a thin wrapper.
5. Verify no dynamic/runtime import still references it (plugins, config strings).

## Supply chain

- Commit lockfiles; use `npm ci`/`pip install --require-hashes`/equivalent for reproducible
  installs.
- Do not run install scripts from untrusted packages with CI secrets available.
- Prefer packages with provenance/attestations where the ecosystem supports it.
- Watch for typosquatting and brand-new packages with suspicious names.
- Enable 2FA and scoped tokens for maintainers; rotate publish credentials.
- Audit regularly and triage by reachability, not just CVSS.
- Keep base images and runtimes patched; dependencies are only part of the surface.

## License guidance

| License | Typical implication |
| --- | --- |
| MIT / BSD / Apache-2.0 | Generally safe; keep notices |
| ISC / 0BSD | Permissive; keep notices |
| MPL-2.0 | File-level copyleft; review modifications |
| LGPL | Dynamic linking usually OK; static/relink obligations need review |
| GPL / AGPL | Strong copyleft; legal review before distribution/SaaS use |
| Unlicensed / custom | Treat as unusable until clarified |

This is not legal advice. Escalate ambiguous or copyleft licenses to the owner.

## Gotchas

- **Install size ≠ bundle size.** A huge dev dependency may not ship; a small package may
  pull a large runtime tree.
- **Duplicate versions** bloat bundles and create type/runtime mismatches. Use the ecosystem's
  dedupe/overrides mechanism deliberately.
- **Peer dependencies** can silently install a second copy of a framework.
- **Native modules** break cross-platform builds and CI images; check prebuilt binaries.
- **Abandoned packages still pass audits** until a CVE lands. Maintenance signals matter.
- **Transitive packages can be compromised.** You are responsible for the whole tree.
- **A wrapper can outlive its value.** If the package only saved five lines, replace it.
- **Lockfile churn hides real changes.** Review it with the manifest, not separately.
- **Dev dependencies can execute code** during install/test in CI. Treat them as code.

For commands, evaluation prompts, and ecosystem specifics, read
[references/dependency-evaluation.md](references/dependency-evaluation.md).

## Output contract

```markdown
## Decision
[Add / keep / replace / remove] — [package] — [one-sentence reason]

## Evaluation
| Criterion | Finding |
| --- | --- |
| Function | [...] |
| Maintenance | [...] |
| Security | [...] |
| Size | [...] |
| License | [...] |
| Transitive tree | [...] |
| Exit cost | [...] |

## Change
[Manifest/lockfile diff, adapter, tests.]

## Verification
[Audit, build, bundle/image size, tests.]

## Follow-ups
[Update cadence, removal date, license review.]
```

## Quality gate

- [ ] The dependency has a stated reason that beats platform/build alternatives.
- [ ] Maintenance, security, license, and size were checked.
- [ ] The transitive tree and install scripts were reviewed.
- [ ] The lockfile is committed and the install is reproducible.
- [ ] Imports are minimal; the API is wrapped if broad.
- [ ] Unused/duplicate packages were removed or justified.
- [ ] The audit was run and findings triaged by reachability.
- [ ] There is an update cadence and an exit path.
