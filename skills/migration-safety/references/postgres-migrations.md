# PostgreSQL Migration Reference

Use with the migration-safety skill. Verify behavior on the target PostgreSQL version; lock
levels and optimizer behavior can change between majors.

## Lock levels cheat sheet

| Statement | Lock | Blocks |
| --- | --- | --- |
| `SELECT` | ACCESS SHARE | Only DDL that needs ACCESS EXCLUSIVE |
| `INSERT/UPDATE/DELETE` | ROW EXCLUSIVE | Conflicting writes; not reads |
| `CREATE INDEX` | SHARE | Writes to the table |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Other DDL; allows reads/writes |
| `ALTER TABLE ... ADD COLUMN` (no rewrite) | ACCESS EXCLUSIVE (brief) | Everything, briefly |
| `ALTER TABLE ... SET NOT NULL` | ACCESS EXCLUSIVE | Everything while it validates (unless using a validated check) |
| `ALTER TABLE ... VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE | Other DDL, not reads/writes |
| `DROP COLUMN` | ACCESS EXCLUSIVE (brief) | Everything, briefly |
| `TRUNCATE` | ACCESS EXCLUSIVE | Everything |

`ACCESS EXCLUSIVE` waits behind any open transaction on the table. A single long transaction
can turn a "brief" lock into a full outage because new queries queue behind the waiting DDL.
Always set `lock_timeout` and retry.

## Expand/contract examples

### Add a nullable column

```sql
SET lock_timeout = '3s';
ALTER TABLE orders ADD COLUMN status text;
-- Deploy code that writes and reads it. Backfill separately. Add constraints later.
```

### Add a column with a constant default (PG 11+)

```sql
SET lock_timeout = '3s';
ALTER TABLE orders ADD COLUMN status text NOT NULL DEFAULT 'pending';
```

On PG 11+ this is metadata-only for non-volatile defaults, but it still takes a brief
`ACCESS EXCLUSIVE` lock. On older versions it rewrites the table.

### Add `NOT NULL` without a long lock (PG 12+)

```sql
-- 1. Add a validated check without scanning under an exclusive lock.
ALTER TABLE orders
  ADD CONSTRAINT orders_status_not_null CHECK (status IS NOT NULL) NOT VALID;

-- 2. Validate with a weaker lock.
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_not_null;

-- 3. Set NOT NULL; PG can use the validated check instead of rescanning.
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;

-- 4. Drop the redundant check.
ALTER TABLE orders DROP CONSTRAINT orders_status_not_null;
```

Verify the version supports using a validated check to skip the scan; otherwise plan a
maintenance window or a new-column transition.

### Create an index without blocking writes

```sql
-- Must not run inside a transaction block.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_tenant_created
  ON orders (tenant_id, created_at DESC);

-- Check validity. A failed build leaves an invalid index.
SELECT indexrelid::regclass, indisvalid
FROM pg_index
WHERE indexrelid = 'idx_orders_tenant_created'::regclass;
```

If invalid: `DROP INDEX CONCURRENTLY idx_orders_tenant_created;` and rebuild. Concurrent
builds take longer and use more I/O; run them when the table is not under peak write load.

### Rename a column safely

```sql
-- Deploy 1: add the new column, keep the old one.
ALTER TABLE users ADD COLUMN full_name text;

-- Deploy 2: dual write from the application, backfill, shadow read.
UPDATE users SET full_name = name WHERE full_name IS NULL; -- batched in practice

-- Deploy 3: read full_name; keep writing both.
-- Deploy 4: stop writing name; verify no reads.
-- Deploy 5: drop the old column after the rollback window.
ALTER TABLE users DROP COLUMN name;
```

Do not use `ALTER TABLE ... RENAME COLUMN` on a live system with old code or external
clients unless you control every reader and can deploy atomically.

### Change a column type safely

```sql
-- Avoid ALTER TYPE on large tables (rewrite + exclusive lock).
ALTER TABLE events ADD COLUMN amount_cents bigint;
-- Backfill: amount_cents = round(amount * 100)
-- Dual write, shadow read, switch, then drop the old column.
```

### Add an enum value

```sql
ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'refunded';
```

On older versions the new value cannot be used in the same transaction. Add it in its own
migration/deploy, then use it.

## Backfill template

```sql
-- Run repeatedly until 0 rows remain. Commit per batch.
WITH batch AS (
  SELECT id
  FROM orders
  WHERE status IS NULL
  ORDER BY id
  LIMIT 1000
  FOR UPDATE SKIP LOCKED
)
UPDATE orders o
SET status = 'pending'
FROM batch
WHERE o.id = batch.id
RETURNING o.id;
```

Operational rules:

- Use an indexed predicate; avoid `OFFSET` for progress.
- Keep each batch small enough to commit in well under a second.
- Throttle (e.g., sleep 50–200 ms) and watch replication lag, CPU, locks, and error rate.
- Make it resumable and idempotent; log the last processed key.
- Stop on the first unexpected error; do not skip rows silently.
- Run through a job with a kill switch, not an ad-hoc console session.

## Verification queries

```sql
-- Long-running transactions that can block DDL
SELECT pid, now() - xact_start AS age, state, query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY age DESC;

-- Locks and blockers
SELECT blocked.pid, blocking.pid, blocked.query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid));

-- Constraint validation
SELECT conname, convalidated
FROM pg_constraint
WHERE conrelid = 'orders'::regclass;

-- Index validity and usage
SELECT indexrelid::regclass, indisvalid, idx_scan
FROM pg_index
JOIN pg_stat_user_indexes USING (indexrelid)
WHERE indrelid = 'orders'::regclass;

-- Replication lag (primary)
SELECT client_addr, state, sent_lsn, replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

## Rollback strategy

- **Schema additions** are usually safe to leave in place; roll back the code, not the column.
- **Destructive changes** (drop/truncate/type rewrite) need a backup or export before running.
- **Backfills** should be reversible only if you kept the old value or a mapping; otherwise
  treat them as forward-only and validate before switching reads.
- **Feature flags** are the cheapest rollback for behavior; use them until the data is
  proven correct.
- **Never** write a down-migration that silently drops data just to make rollback easy.
