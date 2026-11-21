# Web Threat Checklist

Load this when reviewing a public web app, API, or multi-tenant product. Use it to prompt
inspection, not to generate a wall of findings. Only report items with a plausible path to
impact.

## Authentication

- [ ] Passwords hashed with Argon2id/bcrypt/scrypt, per-user salt, sane cost.
- [ ] Password policy length-first; no forced composition rules; breach check optional.
- [ ] Login/reset/OTP rate-limited per account and per IP; generic responses.
- [ ] Reset tokens single-use, short-lived, bound to the user, invalidated on use.
- [ ] Sessions rotated on login; invalidated on logout, password change, role change.
- [ ] Cookies: `HttpOnly`, `Secure`, `SameSite`; `__Host-` prefix where possible.
- [ ] JWT: signature verified, `alg` allowlisted, `exp`/`nbf`/`aud`/`iss` checked, revocable.
- [ ] OAuth: `state` validated, PKCE for public clients, redirect URI exact-match allowlist.
- [ ] MFA for admins; recovery codes hashed and single-use.
- [ ] Service credentials scoped, rotated, and not shared across environments.

## Authorization

- [ ] Default-deny route policy; new endpoints require an explicit permission.
- [ ] Object access scoped by owner/tenant in the query, not by an ID from the request.
- [ ] Role changes take effect immediately (no stale session claims).
- [ ] Admin actions separately authorized and audited.
- [ ] Bulk/batch endpoints cannot mix tenants.
- [ ] Background jobs and webhooks enforce the same scope as the initiating request.
- [ ] GraphQL: resolver-level authz, query depth/cost limits, no field-level leaks.
- [ ] Direct object references tested with a second account (IDOR).

## Injection

- [ ] SQL parameterized everywhere; no concatenated identifiers/`ORDER BY`.
- [ ] ORM raw fragments parameterized; no user input in `whereRaw`/`extra`.
- [ ] NoSQL operators rejected from user JSON; type validation enforced.
- [ ] Shell commands avoid user input; argument arrays; allowlists.
- [ ] HTML escaped by default; sanitizer for allowed rich text; no `dangerouslySetInnerHTML`
      with user content.
- [ ] Path traversal prevented by resolving and checking the root.
- [ ] Redirects and outbound URLs allowlisted; no arbitrary fetch (SSRF).
- [ ] Template injection blocked (no user-controlled template source).
- [ ] Deserialization of untrusted data avoided.
- [ ] Regex input bounded; no user-controlled patterns.
- [ ] CSV exports escape cells starting with `= + - @`.

## CSRF, CORS, headers

- [ ] State-changing cookie-auth requests have CSRF tokens or strict origin checks.
- [ ] CORS allowlist is explicit; credentials not combined with `*`.
- [ ] CSP present and not bypassable with `unsafe-inline`/wildcards.
- [ ] `X-Content-Type-Options: nosniff`, `Referrer-Policy`, HSTS, frame-ancestors.
- [ ] `Host`/`X-Forwarded-*` not trusted for auth or URL generation.
- [ ] Clickjacking protection for sensitive actions.

## Sessions and tokens

- [ ] Session ID entropy sufficient; stored hashed where feasible.
- [ ] Idle and absolute timeouts appropriate to risk.
- [ ] Concurrent session policy defined; "log out everywhere" works.
- [ ] API keys scoped, hashed at rest, shown once, revocable, rate-limited.
- [ ] Tokens not placed in URLs (logs, referrers, history).

## Data exposure

- [ ] Responses return only fields the client needs; no mass assignment.
- [ ] Serializers do not leak password hashes, internal flags, or other tenants' data.
- [ ] Errors do not include stack traces, SQL, internal hosts, or secrets.
- [ ] Logs exclude passwords, tokens, full PII, and payment data.
- [ ] Exports and support tools respect permissions and are audited.
- [ ] Cache keys include tenant/user scope; `Cache-Control` on private data.
- [ ] Backups encrypted and access-controlled.

## Uploads and downloads

- [ ] Size/count limits enforced before reading the body.
- [ ] Content validated by magic bytes, not filename/`Content-Type`.
- [ ] Images re-encoded; SVG sanitized or served as attachment.
- [ ] Stored outside web root or in object storage with random keys.
- [ ] Served with safe `Content-Type` and `Content-Disposition`.
- [ ] Malware scanning for shared files.
- [ ] No path traversal in download handlers; authorize each file.

## SSRF and outbound

- [ ] Destination allowlist by scheme/host.
- [ ] Resolved IP checked; block private, loopback, link-local, metadata ranges.
- [ ] Redirects not followed blindly; re-validate each hop.
- [ ] Timeouts and response size limits.
- [ ] No response body returned verbatim to the user (blind SSRF mitigation).

## Abuse and availability

- [ ] Rate limits on auth, search, export, invite, and expensive endpoints.
- [ ] Pagination and query complexity bounded.
- [ ] Request body and header size limits.
- [ ] Idempotency for retryable mutations.
- [ ] Queue/backpressure for async work; no unbounded fan-out.
- [ ] Account enumeration avoided in signup/reset/invite flows.

## Dependencies and supply chain

- [ ] Audit run and findings triaged by reachability.
- [ ] Lockfile committed; installs reproducible.
- [ ] New packages checked for maintenance, provenance, install scripts, license.
- [ ] Unused packages removed.
- [ ] CI does not expose secrets to untrusted PRs or install scripts.

## Multi-tenancy specifics

- [ ] Every table with tenant data has a tenant key and a constraint/index.
- [ ] Row-level security (if used) is enabled and tested, not assumed.
- [ ] Tenant context is set explicitly per request/job; no global mutable tenant.
- [ ] Cross-tenant access attempts are logged and alerted.
- [ ] Tenant deletion/export is complete and authorized.
