---
name: performance-engineering
description: "Make software faster with measurements, not guesses: define a budget, profile the real hot path, fix the dominant cost (algorithm, I/O, N+1, payload, render), and prove the win with before/after numbers. Use when something is slow, when optimizing a page, API, query, build, or bundle, or when reviewing code for performance risk. Prevents premature optimization, fake wins, and optimizations that only move the cost elsewhere."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: performance
  standard: agentskills.io
---

# Performance Engineering

Performance is a product requirement with a number attached. Without a number, "faster" is
an opinion. Without a profile, the optimization is a guess. The loop is always:

**Define budget → measure → find the dominant cost → change one thing → measure again.**

## Non-negotiables

1. **No optimization without a baseline.** Capture before-numbers from a realistic workload.
2. **Optimize the bottleneck, not the code you enjoy.** A 90% win on 2% of the time is noise.
3. **Measure the user-visible metric**, not just CPU or a micro-benchmark.
4. **Change one variable at a time.** Otherwise you cannot attribute the win or the regression.
5. **Keep correctness and readability.** A fast wrong answer is worse than a slow right one.
6. **Add a guard.** A benchmark or budget check prevents the next regression.

## Workflow

### 1. Define the metric and the budget

Pick the metric that matches the user pain:

| Layer | Metrics |
| --- | --- |
| Web page | LCP, INP, CLS, TTFB, JS bundle KB, hydration time |
| API | p50/p95/p99 latency, throughput, error rate, payload bytes |
| Database | query p95, rows scanned, calls per request, lock wait |
| Job/queue | lag, duration p95, retries, backlog |
| Build/CI | wall time, cache hit rate, image size |
| Mobile/native | cold start, frame time, memory, network bytes |

Write the target as a testable statement: "Orders API p95 < 300 ms at 100 rps on production
data volume." If the user has no target, propose one based on current behavior and the cost
of the pain. Do not chase "as fast as possible".

### 2. Measure a realistic baseline

- Use production-like data volume, concurrency, and cache state.
- Measure warm and cold paths separately.
- Capture p50/p95/p99, not just averages; averages hide the users who suffer.
- Record the environment: hardware, version, flags, dataset, run count.
- Run enough iterations to separate signal from noise; report variance.
- For frontend, use field data (RUM) when available, lab data (Lighthouse/WebPageTest)
  otherwise. They answer different questions.

If you cannot measure the real system, build the closest safe reproduction and state its
limits.

### 3. Profile to find the dominant cost

Use a profiler, not intuition:

- **CPU:** sampling profiler, flame graph. Look for the widest stack, not the most calls.
- **I/O:** trace spans; count queries, round trips, and serialization time.
- **Database:** `EXPLAIN (ANALYZE, BUFFERS)`, slow query log, calls per request.
- **Browser:** Performance panel, long tasks, layout shifts, network waterfall, bundle
  analyzer.
- **Node/Python:** CPU profile, event-loop lag, async hooks/traces.
- **Memory:** heap snapshot, allocation profile, GC pauses.

Rank costs. The top item is your target; do not optimize item #7 because it is easy.

### 4. Choose the fix by cost class

| Dominant cost | First fixes |
| --- | --- |
| Too many round trips | Batch, join, `IN`/`DataLoader`, parallelize independent calls |
| Too much data | Select only needed columns, paginate, compress, project at the edge |
| Repeated work | Cache with a correct key/TTL, memoize per request, precompute |
| Slow algorithm | Better complexity, index, early exit, avoid repeated scans |
| Blocking work | Move to background, stream, make async, offload CPU |
| Serialization | Smaller payload, binary format, avoid double parse/stringify |
| Browser render | Reduce JS, split bundles, virtualize lists, stabilize props/keys |
| Layout thrash | Batch reads/writes, use `transform`/`opacity`, avoid forced reflow |
| Cold start | Reduce imports, lazy load, warm pools, smaller images |
| Lock contention | Shorten transactions, reorder writes, partition, retry with jitter |

Prefer the fix that removes work over the fix that hides it. Caching hides a slow path;
fixing the query removes it. Use caching when the underlying work is legitimately expensive
and invalidation is understood.

### 5. Implement the smallest effective change

- Keep behavior identical; verify with tests.
- Do not add a cache, queue, or service unless the measurement justifies the operational cost.
- Make the change observable: add the metric/trace that proves it.
- If the fix adds complexity, document the budget it protects and the condition to revisit.

### 6. Measure again and report honestly

Report a table, not a adjective:

```
Metric            Before      After      Change
orders p95        820 ms      240 ms     -71%
queries/request   41          3          -93%
payload           1.8 MB      210 KB     -88%
```

State the environment, run count, and variance. If the win is within noise, say so. If the
change moved the cost (e.g., faster API but stale data), report the trade-off.

### 7. Add a guard

- A benchmark in CI with a threshold and a stable dataset.
- A bundle-size budget for the frontend.
- A query-count assertion for critical endpoints.
- A load test on a schedule, not on every commit.
- An alert on the user-facing SLO.

Use `scripts/perf_gate.py` to compare two metric snapshots against a budget. It exits
non-zero on regression, so it can run in CI:

```bash
python scripts/perf_gate.py before.json after.json --budget budget.json
```

Input format:

```json
{"metrics": {"api.orders.p95_ms": 240, "web.lcp_ms": 2100}}
```

Budget format:

```json
{
  "api.orders.p95_ms": {"max": 300, "max_regression_pct": 10},
  "web.lcp_ms": {"max": 2500}
}
```

## Profiling gotchas

- **Averages lie.** A p50 of 100 ms with a p99 of 4 s is a broken product for the tail.
- **Warm cache is not the real path.** Measure cold starts and cache misses.
- **Local hardware is not production.** Network, disk, and noisy neighbors change the shape.
- **Micro-benchmarks mislead.** JIT warmup, dead-code elimination, and unrealistic inputs
  can invert the ranking. Validate in the real system.
- **Observability has a cost.** High-cardinality metrics and verbose tracing can slow the
  thing you are measuring; sample.
- **N+1 hides in serializers.** A clean controller can trigger one query per item in a
  serializer/view.
- **Indexes are not free.** They slow writes and consume memory; verify the query uses them.
- **Caching adds a consistency problem.** A fast stale answer may be worse than a slow fresh
  one. Define invalidation before adding a cache.
- **Parallelism has limits.** More workers can increase contention, memory, and tail latency.
- **Compression trades CPU for bytes.** Measure both sides, especially for small payloads.

## Review checklist for performance risk

- [ ] New query inside a loop? (N+1)
- [ ] Unbounded `SELECT *`, export, or list without pagination?
- [ ] New filter/sort without an index?
- [ ] Work that can be done once per request done per item?
- [ ] Blocking I/O or CPU on the event loop/request path?
- [ ] Payload includes fields the client does not use?
- [ ] New client dependency or large import in the initial bundle?
- [ ] Cache key includes tenant/user and is invalidated on write?
- [ ] Retries/timeouts can amplify load during an incident?
- [ ] The claimed improvement has before/after numbers?

For stack-specific techniques, read
[references/performance-playbook.md](references/performance-playbook.md) when the task
involves a web frontend, HTTP API, or relational database.

## Output contract

```markdown
## Budget
[Metric, target, workload, environment.]

## Baseline
| Metric | Value | Notes |
| --- | --- | --- |

## Bottleneck
[Profile evidence: flame graph, query plan, trace, bundle report.]

## Change
[What changed and why it targets the dominant cost.]

## Result
| Metric | Before | After | Change |
| --- | --- | --- | --- |

## Trade-offs and guard
[Consistency, memory, complexity, cost. Benchmark/alert added.]

## Not done
[Optimizations considered and rejected, with reason.]
```

## Quality gate

- [ ] The target metric and budget are explicit.
- [ ] Baseline and result use the same realistic workload and environment.
- [ ] The profile identifies the dominant cost; the fix targets it.
- [ ] p95/p99 and variance are reported, not just an average.
- [ ] Correctness is unchanged and tests pass.
- [ ] The win is outside noise, with numbers.
- [ ] Trade-offs (staleness, memory, complexity, cost) are stated.
- [ ] A guard prevents regression.
