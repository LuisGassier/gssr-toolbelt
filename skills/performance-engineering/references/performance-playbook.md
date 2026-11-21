# Performance Playbook

Stack-specific techniques. Read the section that matches the work; do not apply all of them.

## Web frontend

### Measure

- Field: Core Web Vitals from RUM (LCP, INP, CLS), segmented by device and route.
- Lab: Lighthouse/WebPageTest for repeatable comparisons; Performance panel for long tasks.
- Bundle: `source-map-explorer`, `webpack-bundle-analyzer`, `vite-bundle-visualizer`.
- Network: waterfall, request count, transferred bytes, cache hit rate.

### Common wins

- Ship less JavaScript: remove unused deps, code-split by route, defer non-critical work.
- Render less: virtualize long lists, memoize expensive subtrees, avoid unstable props/keys.
- Avoid layout thrash: batch DOM reads/writes; animate `transform`/`opacity` only.
- Optimize images: correct dimensions, modern formats, `srcset`, lazy load below the fold.
- Fonts: `font-display: swap`, subset, preload only the critical face.
- Data: fetch in parallel, stream, cache at the edge, avoid waterfalls.
- Third parties: defer/deny tags that do not earn their cost; measure their main-thread time.
- SSR/hydration: reduce hydrated surface, avoid mismatched markup, stream where supported.

### Gotchas

- `useMemo` everywhere adds overhead and hides the real cost.
- A smaller bundle can be slower if it blocks the critical path.
- Lazy loading can hurt LCP if the hero content is deferred.
- Layout animation on `top/left/width/height` forces reflow; use transforms.
- Client-side caching can serve stale data after a mutation; define invalidation.
- INP is about responsiveness, not total JS size; long tasks and input handlers matter.

## HTTP API

### Measure

- p50/p95/p99 latency by route and status; throughput; error rate; payload bytes.
- Distributed traces: time in gateway, app, database, cache, and downstream calls.
- Query count per request (N+1 detection).
- Event-loop lag / thread pool saturation / GC pauses.
- Load test with realistic concurrency and data volume; include cold and warm runs.

### Common wins

- Fix N+1: join, batch, `IN`, or a per-request loader.
- Select only needed columns; avoid `SELECT *` on wide tables.
- Paginate lists; use cursor pagination for large/stable datasets.
- Cache idempotent reads with a key that includes tenant/user and a clear TTL.
- Move slow side effects (email, PDF, image, webhook) to a queue.
- Compress responses; avoid double serialization.
- Use connection pooling; tune pool size to the database, not to hope.
- Add timeouts and bounded retries with jitter; fail fast instead of queueing forever.
- Stream large responses instead of building them in memory.

### Gotchas

- Caching per user without scoping leaks data across tenants.
- Retries without idempotency duplicate writes and amplify outages.
- A larger pool can reduce throughput by contending on the database.
- Compression is not free for tiny or already-compressed payloads.
- Async does not make CPU-bound work faster; it just moves the blocking.

## Relational database (PostgreSQL-oriented)

### Measure

- `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` for the real query and parameters.
- Slow query log / `pg_stat_statements` by total time, not just mean.
- Rows scanned vs rows returned; index usage; sort/hash spill.
- Locks and wait events; long transactions; bloat and autovacuum.
- Calls per request from the application, not just query time.

### Common wins

- Add a composite index matching the filter and sort order (`tenant_id, created_at`).
- Avoid functions on indexed columns in `WHERE` (use ranges or expression indexes).
- Replace `OFFSET` pagination on large tables with keyset pagination.
- Select only needed columns; avoid wide rows and unnecessary joins.
- Batch inserts/updates instead of one statement per row.
- Use `EXISTS` instead of `COUNT(*)` when only presence matters.
- Precompute expensive aggregates when read-heavy and staleness is acceptable.
- Partition very large tables by time/tenant when pruning is the bottleneck.

### Gotchas

- An index can be ignored due to type mismatch, low selectivity, or stale statistics.
- `COUNT(*)` on a large table is expensive; cache or approximate when possible.
- `ORDER BY random()` scans and sorts the whole set.
- `LIKE '%term%'` cannot use a B-tree; use trigram/full-text search.
- A transaction held open during a network call blocks vacuum and locks.
- Adding an index on a live table can lock writes (use concurrent creation).
- Query plans change with data distribution; re-check after growth.

## Node.js / Python services

- Find event-loop blocking (sync fs, crypto, JSON of huge payloads, CPU loops).
- Use streaming for large bodies; enforce size limits.
- Bound concurrency for fan-out and background work.
- Reuse clients/connections; do not create a pool per request.
- Watch memory growth: leaks, unbounded caches, listeners, buffers.
- Profile CPU and heap; do not guess from code shape.
- In Python, watch GIL-bound CPU work and thread pools for I/O; use processes for CPU.
- In Node, unhandled promise rejections and listener leaks are performance bugs too.

## Build and CI

- Cache dependencies and build artifacts with correct keys.
- Parallelize independent jobs; avoid serializing the whole pipeline.
- Shard tests by runtime; quarantine slow/flaky suites.
- Measure wall time and queue time separately.
- Keep the critical path small; move non-blocking checks off the merge path.
