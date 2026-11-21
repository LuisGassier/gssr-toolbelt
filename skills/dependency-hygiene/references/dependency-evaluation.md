# Dependency Evaluation Reference

Commands and prompts by ecosystem. Run them in the repo; do not trust a package's README alone.

## Universal evaluation prompts

1. What exactly do we use from this package? Can we import only that part?
2. What did the last 6–12 months of releases look like? Security fixes? Breaking churn?
3. How many transitive packages does it add? Any native builds or install scripts?
4. What is the license, and does it fit our distribution model?
5. What happens if it is abandoned tomorrow? Can we replace it behind an adapter?
6. Is there a platform/stdlib/existing-dependency alternative?
7. What is the runtime/bundle cost on the devices we support?
8. Are there open critical advisories or unresolved security issues?

## JavaScript / TypeScript

```bash
# What is installed, and why
npm ls <package>
npm ls --all
npm explain <package>

# Outdated and duplicate versions
npm outdated
npm dedupe
npm ls <package> --all

# Unused dependencies
npx depcheck

# Audit (triage by reachability, not just severity)
npm audit
npm audit --production

# Bundle impact (if built with a bundler)
npx source-map-explorer dist/assets/*.js
npx vite-bundle-visualizer
# or check package size before installing:
# https://bundlephobia.com / https://pkg-size.dev

# Install scripts and provenance
npm view <package> scripts dist.tarball repository
npm view <package> time --json
```

Check `package.json` for:

- Unpinned ranges (`*`, `latest`) in production dependencies.
- Duplicate major versions of React/framework packages.
- Dev dependencies that ship in the runtime bundle.
- `postinstall`/`prepare` scripts in untrusted packages.
- Overrides/resolutions used to patch a transitive issue without a plan.

## Python

```bash
pipdeptree
pipdeptree --reverse --packages <package>
python -m pip list --not-required
pip-audit
pip-audit -r requirements.txt
python -m pip show <package>
```

Check `pyproject.toml`/`requirements.txt` for unpinned versions, duplicate constraints,
platform-specific wheels, and packages that shadow stdlib names. Prefer `uv`/`pip-tools`
lockfiles for reproducibility.

## Go

```bash
go mod why ./...
go mod graph
go mod tidy
go list -m -u all
govulncheck ./...
```

Check for replace directives, pseudo-versions, and modules that pull large trees.

## Rust

```bash
cargo tree
cargo tree -d          # duplicates
cargo machete          # unused
cargo audit
cargo outdated
```

Check for multiple versions of the same crate, native `-sys` crates, and build scripts.

## Ruby / PHP / Java

- Ruby: `bundle outdated`, `bundle audit`, `bundle viz`.
- PHP: `composer outdated`, `composer audit`, `composer why <package>`.
- Java/Kotlin: dependency insight in Gradle/Maven, OWASP dependency-check, `mvn dependency:tree`.

## License quick reference

| License | Obligation |
| --- | --- |
| MIT, BSD-2/3, ISC, 0BSD | Keep copyright/license notice |
| Apache-2.0 | Keep notice, state changes, patent grant |
| MPL-2.0 | File-level copyleft; publish changes to MPL files |
| LGPL-2.1/3.0 | Dynamic linking usually allowed; relinking/notice obligations |
| GPL-2.0/3.0 | Derivative works must be GPL if distributed; legal review |
| AGPL-3.0 | Network use can trigger source disclosure; legal review |
| Unlicensed | No permission granted; do not use without clarification |

This is not legal advice. Escalate copyleft or ambiguous licenses.

## Supply-chain checklist

- [ ] Lockfile committed; CI uses a frozen install (`npm ci`, `--frozen-lockfile`, hashes).
- [ ] Install scripts reviewed; secrets not exposed to untrusted scripts.
- [ ] New packages checked for typosquatting and recent ownership changes.
- [ ] Publish credentials use 2FA and least privilege.
- [ ] Base images and runtimes pinned and patched.
- [ ] Audit findings triaged by reachability and exploitability.
- [ ] No `curl | bash` installers in build scripts.
- [ ] Dependency updates have an owner and a cadence.
