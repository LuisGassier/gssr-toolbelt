---
name: observability-first
description: "Instrument software so production problems are debuggable: structured logs, metrics, traces, request IDs, SLOs, symptom-based alerts, and runbooks. Use when adding a service, endpoint, job, or integration; when debugging production; or when asked about logging, monitoring, metrics, tracing, alerting, or on-call readiness. Builds observability into the change instead of bolting it on after an incident."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: operations
  standard: agentskills.io
---

# Observability First

Observability is the ability to answer new questions about production without shipping new
code. Logs, metrics, and traces are the raw material; the goal is answers:

- Is the service healthy right now?
- Who is affected, and how badly?
- What changed?
- Where is the time or error coming from?
- Is it getting better or worse?

Instrument while building. Retrofitting observability during an incident is how you get
dashboards nobody trusts and alerts nobody reads.

## Non-negotiables

1. **Every request/job has a correlation ID** propagated across services and logs.
2. **Logs are structured events**, not prose. They carry fields, not interpolated strings.
3. **No secrets or PII in logs, traces, metrics labels, or error messages.**
4. **Alert on user-visible symptoms**, not on every internal cause.
5. **Every alert has an owner, a runbook, and a clear action.**
6. **Metrics labels are low-cardinality.** Never put user IDs, emails, or raw URLs in labels.

## Workflow

### 1. Name the critical journeys

List the few flows that matter: login, checkout, search, ingest, sync, publish. For each,
define what "working" means in user terms and the signal that proves it.

```
Journey: checkout
Success: order confirmed, payment captured, receipt sent
SLI: proportion of checkout requests that return 2xx and emit order_confirmed
Target: 99.9% over 30 days
```

### 2. Instrument the boundaries

Add telemetry at the edges where failures and latency accumulate:

- Inbound HTTP/RPC/GraphQL: route, method, status, duration, request ID.
- Outbound calls: dependency, operation, status, duration, retries.
- Database: query name, duration, rows, errors (not raw SQL with values).
- Queue/job: enqueue, start, duration, retries, dead-letter, lag.
- Auth: success/failure reason code (not credentials), permission denials.
- Business events: signup, order, payment, invite, export.

Use the framework's middleware/plugin where possible. Do not hand-roll a logging pipeline in
every handler.

### 3. Logs

Use one structured format (JSON or logfmt). A useful event has:

```json
{
  "ts": "2026-11-21T10:15:30.123Z",
  "level": "error",
  "service": "orders-api",
  "env": "prod",
  "version": "2026.11.21-1",
  "request_id": "01J8...",
  "trace_id": "4bf92f...",
  "tenant_id": "t_123",
  "event": "order.create.failed",
  "duration_ms": 412,
  "error_code": "payment_declined",
  "message": "payment provider declined the charge"
}
```

Rules:

- Log **events**, not sentences: `order.create.failed` plus fields.
- Use levels consistently: `debug` (off in prod), `info` (state changes), `warn` (degraded
  but handled), `error` (needs attention), `fatal` (process cannot continue).
- Log the decision and the outcome, not every function entry.
- Include IDs needed to join with traces and other services.
- Never log passwords, tokens, full card numbers, authorization headers, or raw PII. Hash or
  redact identifiers if you need correlation.
- Bound message size; do not log entire payloads or base64 blobs.
- Do not log in tight loops; sample or aggregate.

### 4. Metrics

Use a small, standard set:

- **RED** for request-driven services: Rate, Errors, Duration (p50/p95/p99).
- **USE** for resources: Utilization, Saturation, Errors (CPU, memory, connections, queue).
- **Business**: signups, orders, payments, invites, exports — the numbers the product cares
  about.
- **Dependencies**: per-dependency latency/error rate, retries, circuit state.

Naming:

```
http_server_request_duration_seconds{route,method,status}
http_server_requests_total{route,method,status}
db_query_duration_seconds{operation,table}
queue_depth{queue}
job_duration_seconds{job,status}
```

Rules:

- Include units in the name (`_seconds`, `_bytes`, `_total`).
- Keep label cardinality bounded. Route templates, not raw paths. Status classes, not every
  code, unless needed.
- Do not label by user, email, request ID, or free-text error message.
- Use histograms for latency; averages hide the tail.
- Add exemplars/trace links where the platform supports them.

### 5. Traces

- Propagate context (W3C `traceparent`) across HTTP, queues, and jobs.
- Name spans by operation (`GET /orders/:id`, `db.orders.select`), not by code function.
- Record the attributes needed to debug: route, status, dependency, retry count, tenant
  (pseudonymous), not payloads.
- Sample deliberately: head-based for volume, tail-based for errors/slow requests if
  available.
- Ensure async work continues the trace; do not start a new root span for a job spawned by a
  request.

### 6. SLOs and alerts

Define SLIs from the user's perspective, then set an SLO and an error budget. Alert on burn
rate, not on a single spike:

- Fast burn: 2% of the 30-day budget in 1 hour → page.
- Slow burn: 10% in 6 hours → ticket.
- Include a short window and a long window to avoid flapping.

Alert rules:

- **Symptom-based:** high error rate, high latency, failed checkout, queue lag.
- **Actionable:** the responder can do something. If not, it is a dashboard, not a page.
- **Owned:** team, severity, runbook link, dashboard link.
- **Deduplicated:** group by service/route, not per instance.
- **Tested:** send a synthetic failure and confirm the alert fires and routes correctly.
- Do not page on CPU alone, a single 5xx, a disk at 70%, or a deploy event.

### 7. Dashboards and runbooks

A good dashboard answers the three questions in order:

1. **Is it broken?** SLO/error rate/latency at the top.
2. **Where?** By route, dependency, region, tenant tier.
3. **What changed?** Deploys, flags, migrations, traffic, dependency status.

Every alert links to a runbook with:

- What the alert means and its user impact.
- First five checks (dashboard, logs, traces, recent deploys, dependency status).
- Mitigation: rollback, flag off, scale, failover, rate-limit.
- Escalation and communication.
- How to verify recovery.

### 8. Verify observability

Before calling the work done, answer these using only telemetry:

- Can I tell a request succeeded end-to-end?
- Can I find the slowest span for a specific failing request?
- Can I see which tenant/route is affected without reading raw payloads?
- Can I correlate a deploy with a change in error rate?
- Does the alert fire in a test, and does it include the runbook?
- Can I debug without SSH or a database console?

If any answer is no, the instrumentation is incomplete.

## Anti-patterns

- `console.log`/`print` as the production logging strategy.
- Unstructured messages with interpolated values (`User ${email} failed`).
- Logging every request at `info` with full headers and bodies.
- High-cardinality metric labels (user ID, email, URL with IDs).
- One alert per cause, all paging, none actionable.
- Dashboards with 40 panels and no owner.
- Metrics without units or percentiles.
- Traces that stop at the service boundary.
- Sampling that drops all errors.
- SLOs with no error budget or consequence.
- "We'll add monitoring later" in a launch plan.

## Gotchas

- **Log volume can be the outage.** A retry loop logging at `error` can saturate the log
  pipeline and the disk. Rate-limit repeated errors.
- **PII hides in URLs and error objects.** Query strings, headers, and exception messages can
  contain tokens or emails. Redact at the logger boundary.
- **Cardinality explosions are silent until the bill arrives.** A new label with tenant ID can
  multiply every time series.
- **Async context can be lost.** Background jobs, queue consumers, and thread pools need
  explicit context propagation.
- **Clock skew breaks correlation.** Use UTC and trust the collector's timestamp where
  possible.
- **Symptom alerts still need cause dashboards.** Page on the symptom; make the cause easy to
  find.
- **Sampling can hide the long tail.** Keep 100% of errors and slow traces if the backend
  supports it.
- **A green dashboard is not proof.** Check that the signal is actually emitted on the success
  path, not only on failure.

For schemas, naming, SLO math, and alert examples, read
[references/instrumentation.md](references/instrumentation.md).

## Output contract

```markdown
## Critical journeys and SLIs
| Journey | SLI | Target | Window |
| --- | --- | --- | --- |

## Instrumentation added
- Logs: [events and fields]
- Metrics: [names, types, labels]
- Traces: [spans and propagation]
- Business events: [...]

## Alerts
| Alert | Symptom | Threshold | Severity | Runbook |
| --- | --- | --- | --- | --- |

## Dashboards
[What question each answers.]

## Verification
[How I proved the signals work, including a synthetic failure.]

## Privacy
[What is redacted or excluded.]
```

## Quality gate

- [ ] Every critical journey has an SLI and a target.
- [ ] Requests/jobs carry a correlation ID across boundaries.
- [ ] Logs are structured, leveled, and free of secrets/PII.
- [ ] Metrics have units, percentiles, and bounded labels.
- [ ] Traces propagate through async work and dependencies.
- [ ] Alerts are symptom-based, actionable, owned, and linked to runbooks.
- [ ] Dashboards answer "broken / where / what changed".
- [ ] Observability was verified with a synthetic failure, not assumed.
