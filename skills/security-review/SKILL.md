---
name: security-review
description: "Threat-model and security-review code, APIs, and data flows: authentication, authorization, tenant isolation, injection, secrets, SSRF, file uploads, sessions, crypto, and dependency risk. Use before shipping anything that touches auth, user data, payments, uploads, admin actions, or the internet; also when auditing an existing app or investigating a suspected vulnerability. Prioritizes exploitable findings over checklist noise."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: security
  standard: agentskills.io
---

# Security Review

Security review is threat modeling plus evidence. The question is not "does this look
secure?" It is: *who can make this system do something it should not, and what stops them?*

Review the paths that touch identity, money, data, and the network first. A missing
`SameSite` cookie on a blog matters less than an unauthenticated delete endpoint.

## Operating rules

- **Authorize on the server, in the data access layer.** Hiding a button is not access
  control. Check every route, job, webhook, and direct object reference.
- **Assume all input is hostile**, including headers, filenames, JSON keys, URLs, and data
  from other services.
- **Treat secrets as compromised if they touch code, logs, client bundles, or git.**
- **Prefer platform primitives** (parameterized queries, vetted crypto, framework auth)
  over hand-rolled checks.
- **Do not run intrusive tests against production.** Use a local/staging copy and safe,
  non-destructive probes.
- **Report exploitable issues, not hypotheticals.** State the attacker, precondition,
  impact, and evidence. Avoid fear-driven checklists with no path to impact.

## Workflow

### 1. Map the attack surface

List entry points and trust boundaries:

- Public HTTP/RPC/GraphQL endpoints, webhooks, websockets.
- Authenticated user actions, admin actions, background jobs, cron, CLI.
- File uploads/downloads, imports, exports, email/push.
- Third-party callbacks, OAuth flows, redirects, outbound fetches.
- Data stores, queues, caches, and internal service calls.

For each, note: who can reach it, what identity is required, what data it touches, and what
happens on failure.

### 2. Build a lightweight threat model

For the highest-risk flows, answer:

```
Asset: [data/action worth protecting]
Actor: [anonymous / user / member / admin / service / insider]
Entry: [route/job/flow]
Trust boundary: [where input crosses into trusted code]
Abuse: [what the actor could do if controls fail]
Control: [authn/authz/validation/rate limit/encryption/audit]
Residual risk: [accepted / needs fix]
```

STRIDE is useful as a prompt, not a deliverable: Spoofing, Tampering, Repudiation,
Information disclosure, Denial of service, Elevation of privilege.

### 3. Authentication

- Are passwords hashed with a memory-hard algorithm (Argon2id/bcrypt/scrypt) and a per-user
  salt? Never SHA-256 alone.
- Are session tokens random, high-entropy, and stored hashed server-side where possible?
- Are cookies `HttpOnly`, `Secure`, and `SameSite=Lax/Strict` as appropriate?
- Is session fixation prevented (rotate on login, invalidate on logout/password change)?
- Are password reset tokens single-use, short-lived, and invalidated after use?
- Is MFA available for privileged accounts? Is step-up required for sensitive actions?
- Are login, reset, and OTP endpoints rate-limited and resistant to user enumeration?
- Is "remember me" a separate, revocable credential?
- Are service-to-service credentials scoped and rotated?

### 4. Authorization and tenant isolation

This is the most common serious bug. For every object access, verify:

- The query includes the tenant/owner scope: `WHERE id = ? AND tenant_id = ?`.
- The permission check happens server-side on every path, not just the UI route.
- Roles are enforced with a default-deny policy; new routes are not accidentally public.
- Admin endpoints are separately authorized and audited.
- IDs are not trusted as proof of ownership (IDOR).
- Bulk operations cannot cross tenant boundaries.
- Background jobs carry and enforce the same scope as the request that scheduled them.
- Cache keys include tenant/user scope where data is not public.

Test the matrix: owner, member, admin, outsider, unauthenticated, deleted/suspended user.

### 5. Injection and input handling

- SQL: parameterized queries only; no string concatenation, including `ORDER BY` and
  identifiers (allowlist those).
- NoSQL: reject operator objects (`$ne`, `$gt`) from user JSON; validate types.
- Shell: avoid shells; if unavoidable, pass argument arrays and allowlist.
- Templates: auto-escaping on; no raw HTML from users; sanitize with a maintained library.
- Paths: resolve and verify the result stays inside the allowed root; reject traversal.
- URLs/redirects: allowlist schemes and hosts; do not fetch arbitrary user URLs (SSRF).
- Deserialization: never deserialize untrusted pickle/Java/PHP objects; prefer JSON with
  a schema.
- Regex: avoid user-controlled patterns (ReDoS); bound input length.
- Headers: validate `Host`, `Origin`, `X-Forwarded-*`; do not trust them for auth.

### 6. Secrets and configuration

- No secrets in source, tests, fixtures, client bundles, or logs.
- Secrets come from a secret manager/env, are scoped, and are rotatable.
- `.env` files are gitignored; `.env.example` contains placeholders only.
- Error responses do not include stack traces, SQL, internal URLs, or keys.
- Debug/verbose modes are off in production.
- Default credentials and sample keys are removed.
- CI logs and artifacts do not leak tokens.

If a secret was committed, rotate it. Deleting the commit is not enough.

### 7. Data protection

- Classify data: public, internal, personal, sensitive (health, payment, credentials).
- Encrypt in transit (TLS, no mixed content) and at rest where required.
- Minimize collection and retention; delete on request and on schedule.
- Do not log PII, tokens, passwords, full request bodies, or payment data.
- Mask sensitive fields in UI, exports, and support tools.
- Backups are encrypted and access-controlled.
- Audit logs record who did what, when, from where — and are append-only.

### 8. Uploads, downloads, and outbound requests

- Validate size, count, and content type; do not trust the filename or `Content-Type`.
- Re-encode images; never serve user uploads from the app origin with executable types.
- Store outside the web root or in object storage with random names.
- Scan for malware if files are shared with other users.
- Force `Content-Disposition: attachment` for untrusted downloads.
- For outbound requests: allowlist hosts/schemes, block link-local/metadata IPs, set
  timeouts, and do not follow redirects blindly (SSRF).

### 9. Browser and API defenses

- CSRF protection for cookie-authenticated state-changing requests (token or
  `SameSite` + origin check).
- CORS is an explicit allowlist, not `*` with credentials.
- Security headers: CSP, `X-Content-Type-Options`, `Referrer-Policy`,
  `Strict-Transport-Security`, frame-ancestors/`X-Frame-Options`.
- Rate-limit auth, search, export, and expensive endpoints; return `429` with `Retry-After`.
- Validate content types and reject unknown fields where the contract is strict.
- Do not expose sequential IDs when enumeration is sensitive; authorize anyway.

### 10. Dependencies and supply chain

- Run the ecosystem audit (`npm audit`, `pip-audit`, `cargo audit`, etc.) and triage by
  reachability, not just severity.
- Remove unused packages; fewer dependencies mean less attack surface.
- Pin lockfiles and review new packages for maintenance, downloads, and install scripts.
- Do not run `postinstall` scripts from untrusted packages in CI with secrets.
- Verify licenses and provenance for new dependencies.

### 11. Logging, monitoring, and response

- Log security-relevant events: login success/failure, permission denial, admin action,
  password/email change, token reuse, rate-limit trips.
- Include request ID, actor, tenant, action, result — never secrets or full PII.
- Alert on anomalies (spike in 401/403, reset abuse, unusual export volume).
- Have a path to revoke sessions/tokens and rotate keys.
- Document how to report a vulnerability and who responds.

## Severity and reporting

| Severity | Criteria | Response |
| --- | --- | --- |
| Critical | Unauthenticated RCE, auth bypass, mass data exposure, payment manipulation | Stop shipping; fix now; assess exposure |
| High | Privilege escalation, tenant data leak, stored XSS with session impact, SSRF to metadata | Block release; fix before deploy |
| Medium | Limited IDOR, CSRF on sensitive action, weak rate limit, verbose errors | Fix next; mitigate if exposed |
| Low | Missing header, minor info leak, hardening gap | Schedule |

For each finding:

```
[Severity] Title
Where: file/endpoint/flow
Actor and precondition: [who, what they need]
Impact: [what they can read/change/break]
Evidence: [request/code path, not a full exploit against prod]
Fix: [specific control]
Verification: [test or check that proves the fix]
```

## Gotchas

- **Authorization in the UI only.** Direct API calls bypass it.
- **Tenant ID from the request body.** Attackers can change it; derive scope from the
  authenticated session.
- **GraphQL field-level leaks.** A single query can traverse to other users' data; authorize
  at the resolver and object level.
- **Webhook trust.** Verify signatures, timestamps, and replay windows; do not trust the
  payload's tenant/user claims.
- **JWT pitfalls.** `alg: none`, weak secrets, missing expiry/audience/issuer checks, and
  tokens that cannot be revoked.
- **SSRF via redirects and DNS rebinding.** Validate the resolved IP, not just the hostname.
- **CSV injection.** Cells beginning with `=`, `+`, `-`, `@` can execute in spreadsheets.
- **Race conditions in authorization.** Check-and-act must be atomic; a user downgraded
  mid-request may still complete an action.
- **Soft-deleted users.** Ensure deleted/suspended accounts cannot authenticate or access
  data through stale tokens.
- **Error messages as an oracle.** Distinguish "not found" from "not allowed" only when it
  does not enable enumeration.

For a deeper checklist by category, read
[references/web-threat-checklist.md](references/web-threat-checklist.md) when the review
covers a public web app, API, or multi-tenant product.

## Output contract

```markdown
## Scope and assumptions
[What was reviewed, what was not, environment.]

## Threat model
| Asset | Actor | Entry | Abuse | Control | Residual |
| --- | --- | --- | --- | --- | --- |

## Findings
### [Critical/High/Medium/Low] [Title]
- Where: [...]
- Precondition: [...]
- Impact: [...]
- Evidence: [...]
- Fix: [...]
- Verification: [...]

## Verified controls
[What is already done well — so the team knows what not to break.]

## Not reviewed
[Areas outside scope or requiring runtime/prod access.]

## Priority
[Order of fixes and whether any block release.]
```

## Quality gate

- [ ] Every new endpoint/object access has a server-side authorization check.
- [ ] Tenant scope is derived from identity, not from user-supplied IDs.
- [ ] All queries are parameterized; identifiers are allowlisted.
- [ ] No secrets or PII in code, logs, errors, or client bundles.
- [ ] Session/cookie/token settings are appropriate and revocable.
- [ ] Uploads, redirects, and outbound fetches are constrained.
- [ ] Findings include actor, impact, evidence, fix, and verification.
- [ ] Release-blocking severity is called out explicitly.
