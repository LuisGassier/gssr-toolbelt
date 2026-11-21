---
name: api-contract
description: "Design and evolve APIs that clients can depend on: resource and naming rules, status codes, error shape, idempotency, pagination, filtering, versioning, deprecation, and backward compatibility. Use when adding or changing endpoints, designing a public or partner API, writing OpenAPI, reviewing an API change for breakage, or fixing inconsistent API behavior. Produces a contract, not just a handler."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: architecture
  standard: agentskills.io
---

# API Contract

An API is a promise to code you do not control. The handler is the easy part; the contract is
what breaks clients at 2 a.m. Design the observable behavior first: resources, errors,
idempotency, pagination, and compatibility.

Default to HTTP + JSON for new APIs unless the domain has a stronger reason (streaming,
binary, realtime). For RPC-style internal APIs, keep the same contract discipline.

## Non-negotiables

1. **Every response is part of the contract**, including errors, empty states, and headers.
2. **Never break a deployed client silently.** Additive changes are safe; removals, type
   changes, and semantic changes are not.
3. **Mutations that can be retried must be idempotent.** Networks fail; clients retry.
4. **Authorization is part of the contract.** Document who can do what, and enforce it
   server-side.
5. **Validate at the boundary.** Reject unknown/invalid input with a specific, stable error.
6. **One error shape everywhere.** Clients should not parse five formats.

## Workflow

### 1. Model resources and operations

- Use nouns for resources: `/orders`, `/orders/{id}`, `/orders/{id}/items`.
- Use HTTP methods for semantics: `GET` read, `POST` create/action, `PUT` full replace,
  `PATCH` partial update, `DELETE` remove.
- Avoid verbs in paths except for genuine actions that are not CRUD (`/orders/{id}/cancel`).
- Nest only one level; promote deeply nested resources to top-level with filters.
- Use plural, lowercase, hyphenated path segments. Pick one case for JSON fields and keep it.
- Do not expose database IDs if a stable public identifier is better; be consistent.

### 2. Define the success contract

For each operation, specify:

- Method and path, auth requirements, required scopes/roles.
- Request schema: required/optional, types, limits, defaults, unknown-field behavior.
- Response schema: every field, nullability, units, timezone, precision.
- Status codes for success and partial success.
- Side effects (emails, jobs, charges) and whether they are synchronous.
- Idempotency behavior and keys.
- Rate limits and pagination.

### 3. Define the error contract

Use RFC 9457 Problem Details (or a single consistent shape):

```json
{
  "type": "https://api.example.com/problems/insufficient-funds",
  "title": "Insufficient funds",
  "status": 409,
  "detail": "The account balance is 12.00 USD; the transfer requires 20.00 USD.",
  "instance": "/transfers/01J8...",
  "code": "insufficient_funds",
  "errors": [
    {"field": "amount", "code": "gt", "message": "must be greater than balance"}
  ]
}
```

Rules:

- Use the right status: `400` malformed, `401` unauthenticated, `403` authenticated but not
  allowed, `404` absent or hidden, `409` conflict, `422` semantically invalid, `429` rate
  limited, `5xx` server fault.
- Do not return `200` with `{"success": false}`. It breaks clients, caches, and monitoring.
- Do not leak stack traces, SQL, internal hosts, or whether a resource exists when that
  enables enumeration.
- Make validation errors field-addressable and machine-readable.
- Keep error codes stable; changing a code is a breaking change.
- Include `Retry-After` for `429`/`503` where the client should wait.

### 4. Idempotency and concurrency

- Support an `Idempotency-Key` header for `POST`/`PATCH` that create or charge.
- Store the key with the request fingerprint and the response for a bounded window.
- Reject reuse of a key with a different payload (`409`).
- Use optimistic concurrency (`ETag`/`If-Match` or a version field) for updates that can
  conflict.
- Define what happens on duplicate creates, double submits, and retries.
- Make webhooks idempotent; deliver at least once, expect duplicates, verify signatures.

### 5. Pagination, filtering, sorting

- Prefer cursor pagination for large or changing datasets:
  `GET /orders?limit=50&cursor=eyJpZCI6...` returning `next_cursor`.
- Offset pagination is acceptable for small/stable sets, but document the consistency limit.
- Cap `limit`; default to a sane page size.
- Return a stable sort order; document the tie-breaker.
- Filters are explicit query params; do not accept arbitrary query languages unless needed.
- Validate filter/sort fields against an allowlist to avoid injection and expensive scans.
- Return total counts only when cheap; otherwise provide `has_more`.

### 6. Versioning and evolution

Prefer additive evolution over version bumps:

- Add optional fields with defaults; never repurpose an existing field.
- Never change a field's type, units, nullability, or meaning in place.
- Never remove a field or endpoint without a deprecation window.
- New enum values are breaking for exhaustive clients; announce them.
- Changing validation to be stricter is breaking; loosening is usually safe.
- Changing default behavior is breaking even if the schema is unchanged.

When a breaking change is unavoidable:

1. Introduce the new version/path alongside the old.
2. Document the migration and the deadline.
3. Emit deprecation headers (`Deprecation`, `Sunset`) and notify consumers.
4. Monitor old-version traffic; remove only when it reaches zero or the deadline passes.
5. Keep the old version long enough for the slowest real consumer, not the ideal one.

### 7. Document the contract

- OpenAPI/Protobuf/GraphQL schema is the source of truth; keep it in the repo.
- Include examples for success, validation error, auth error, conflict, and rate limit.
- Document auth, scopes, rate limits, pagination, idempotency, and webhooks.
- Add a changelog for consumer-visible changes.
- Generate or validate client types from the schema; do not hand-maintain duplicates.
- Contract-test the implementation against the schema in CI.

## Decision table

| Question | Default |
| --- | --- |
| REST vs GraphQL vs RPC | REST/JSON for resource APIs; GraphQL when clients need flexible graph reads; RPC for internal high-throughput calls |
| Cursor vs offset | Cursor for large/changing lists; offset for small stable admin tables |
| Version in path vs header | Path (`/v1`) for public APIs; header/media type for internal evolution |
| Sync vs async | Sync for fast user actions; async (202 + job resource) for long work |
| 404 vs 403 | 404 when existence is sensitive; 403 when the resource is known and permission is the issue |
| PUT vs PATCH | PUT full replace; PATCH partial with explicit null semantics |
| Soft vs hard delete | Soft delete when restore/audit is needed; exclude deleted rows by default |

## Gotchas

- **`PATCH` null semantics.** Does `null` clear a field or mean "unchanged"? Pick one and
  document it; use a separate unset operation if needed.
- **Timezones.** Use ISO 8601 with offset or UTC `Z`; never return local times without one.
- **Money.** Use integer minor units or a decimal string with currency; never floats.
- **Empty vs missing.** `[]`, `null`, and absent mean different things; define them.
- **Enums grow.** Clients that switch exhaustively will break on a new value; warn them.
- **Webhook ordering.** Do not assume order; include event IDs and timestamps for dedupe.
- **Retries and side effects.** A `POST` that sends email or charges money needs idempotency.
- **Caching.** Set `Cache-Control`/`ETag` deliberately; authenticated responses should not be
  shared.
- **Rate limits.** Communicate limits in headers and document the window; do not surprise
  clients with silent drops.
- **GraphQL.** Depth/cost limits, persisted queries, resolver-level authz, and N+1 loaders
  are part of the contract.
- **API gateways.** Timeouts and body limits at the proxy can truncate responses before your
  app sees them; test through the real edge.

## Output contract

```markdown
## Resources and operations
| Method | Path | Auth | Purpose | Success |
| --- | --- | --- | --- | --- |

## Request/response schemas
[Fields, types, required, limits, defaults, examples.]

## Errors
[Status, code, when, response example.]

## Idempotency and concurrency
[Keys, conflict behavior, retry semantics.]

## Pagination/filtering
[Cursor format, limit, sort, allowed filters.]

## Compatibility
[What is additive, what is breaking, deprecation plan.]

## Verification
[Schema validation, contract tests, examples checked.]
```

## Quality gate

- [ ] Every operation has auth, request, response, and error contracts.
- [ ] Error shape and status codes are consistent across the API.
- [ ] Retryable mutations are idempotent or explicitly unsafe.
- [ ] Pagination is bounded and stable; filters are allowlisted.
- [ ] Money, time, null, and empty semantics are explicit.
- [ ] Breaking changes have a version/deprecation plan.
- [ ] The schema is in the repo and contract-tested.
- [ ] A client can implement against the docs without asking questions.
