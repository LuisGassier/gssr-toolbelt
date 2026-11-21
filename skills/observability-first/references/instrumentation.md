# Instrumentation Reference

Schemas, naming, SLO math, and alert patterns. Adapt to the platform; keep the principles.

## Log event schema

| Field | Required | Notes |
| --- | --- | --- |
| `ts` | Yes | RFC 3339 UTC with milliseconds |
| `level` | Yes | debug/info/warn/error/fatal |
| `service` | Yes | Stable service name |
| `env` | Yes | prod/staging/dev |
| `version` | Yes | Deploy SHA or semver |
| `event` | Yes | Dot-delimited event name (`order.create.failed`) |
| `request_id` | If request-scoped | Trace/request correlation |
| `trace_id` / `span_id` | If tracing | W3C trace context |
| `tenant_id` | If multi-tenant | Pseudonymous; never an email |
| `duration_ms` | For operations | Numeric, not a string |
| `status` | For operations | `ok`/`error`/`cancelled` |
| `error_code` | On error | Stable, low-cardinality code |
| `message` | Optional | Human context, no secrets |

Rules: one event per line, no multi-line stack traces without a structured field, no raw
payloads, no `JSON.stringify` of entire request objects.

## Log levels

- `debug`: local diagnostics, off in production by default.
- `info`: state changes worth keeping (order created, invite sent, job completed).
- `warn`: handled degradation (retry succeeded, fallback used, quota near limit).
- `error`: the operation failed and someone may need to act.
- `fatal`: the process cannot continue.

Avoid `error` for expected user errors (validation, 404). Those are `info`/`warn` with a
stable code; otherwise alerts drown.

## Metric naming

```
<namespace>_<subject>_<unit>{labels}
```

Examples:

```
http_server_request_duration_seconds{route,method,status}
http_server_requests_total{route,method,status}
db_client_connections_used{pool}
queue_messages_ready{queue}
job_processing_duration_seconds{job,status}
business_orders_total{plan,status}
```

- Counters end in `_total`.
- Durations end in `_seconds`; sizes in `_bytes`.
- Use histograms for latency; report p50/p95/p99.
- Label cardinality budget: if a label can have >100 values, question it. Route templates,
  not paths; status classes, not every code; error codes, not messages.
- Never label with user/tenant/email/request IDs. Use logs/traces for those dimensions.

## Trace conventions

- Span name: `<operation> <target>` (`GET /orders/:id`, `db.orders.select`,
  `http.client.stripe.charge`).
- Attributes: `http.method`, `http.route`, `http.status_code`, `db.system`, `db.operation`,
  `peer.service`, `retry.count`, `tenant.tier` (not ID).
- Propagate W3C `traceparent`/`tracestate` through HTTP, queues, and async jobs.
- Mark errors with status and a stable error code; do not put exception text in the span name.
- Sample: 100% errors and slow traces if possible; 1–10% of normal traffic for volume.

## SLI and SLO math

- **SLI:** a ratio of good events to valid events.
  `good = requests with status < 500 and duration < 300ms`
  `valid = all non-health-check requests`
- **SLO:** target over a window, e.g., 99.9% over 30 days.
- **Error budget:** `(1 - SLO) × valid events`. At 99.9% and 1M requests/month, the budget is
  1,000 failed requests.
- **Burn rate:** how fast the budget is consumed relative to the window.
  Burn rate 1 = exactly on budget. Burn rate 14.4 = budget exhausted in ~2 days.

Multi-window alerting:

| Severity | Long window | Short window | Burn rate | Action |
| --- | --- | --- | --- | --- |
| Page | 1h | 5m | 14.4 | Fast burn; respond now |
| Page | 6h | 30m | 6 | Sustained burn |
| Ticket | 3d | 6h | 1 | Slow burn; fix this week |

Tune to traffic; low-volume services need longer windows or synthetic checks.

## Alert template

```yaml
alert: CheckoutErrorRateHigh
expr: |
  sum(rate(http_server_requests_total{route="/checkout",status=~"5.."}[5m]))
  /
  sum(rate(http_server_requests_total{route="/checkout"}[5m]))
  > 0.02
for: 10m
labels:
  severity: page
  team: payments
  runbook: https://runbooks.example.com/checkout-error-rate
annotations:
  summary: Checkout 5xx rate above 2% for 10 minutes
  impact: Customers cannot complete purchases
  dashboard: https://dash.example.com/checkout
```

Every alert needs: symptom, threshold, duration, severity, owner, runbook, dashboard, and a
clear first action. If it fires for a cause the responder cannot act on, downgrade it.

## Dashboard layout

1. **Top row:** SLO status, error budget remaining, request rate, error rate, p95/p99.
2. **Second row:** latency by route/dependency, saturation (CPU, memory, pool, queue).
3. **Third row:** deploys/flags/migrations as annotations, dependency status, business metric.
4. **Detail:** per-tenant tier or region if the product is partitioned.

Avoid: 40 panels, averages without percentiles, colors without thresholds, dashboards with no
owner or link from alerts.

## Verification drills

- Send a synthetic 5xx and confirm the alert fires, routes, and includes the runbook.
- Inject latency and confirm the trace shows the slow span and the dashboard moves.
- Trigger a job failure and confirm retry/dead-letter metrics.
- Search logs by `request_id` and reconstruct a request end-to-end.
- Confirm a known secret/PII field is redacted in logs and traces.
- Confirm the success path emits the business event, not only the failure path.
