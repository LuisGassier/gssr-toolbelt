---
name: migration-safety
description: "Plan and execute schema and data migrations without downtime or data loss: expand/contract, backward-compatible deploys, batched backfills, lock awareness, verification, and rollback. Use for database changes, column/table renames, backfills, index creation, data cleanup, or any migration that must run on live production data. Treats migrations as multi-deploy operations, not one-way scripts."
license: MIT
metadata:
  author: gssr-toolbelt
  version: "1.0.0"
  updated: "2026-11"
  domain: data
  standard: agentskills.io
---

# Migration Safety

A migration is not a file you run once. It is a sequence of states that old code, new code,
and live traffic must all survive. The dangerous part is rarely the SQL syntax; it is the
window where two versions of the application disagree about the schema.

Default rule: **expand → migrate → contract**, across separate deploys, with the old path
still working until the new path is proven.

## Non-negotiables

1. **Every migration is backward-compatible with the currently deployed code.** If old code
   breaks during the deploy, you have an outage.
2. **Never rewrite or lock a large table in a request path.** Know the lock each statement
   takes and bound it with timeouts.
3. **Backfill in batches, idempotently, with throttling.** A single `UPDATE` on a large table
   is an outage waiting for a busy day.
4. **Verify data, not just schema.** Row counts, nulls, constraints, and application reads.
5. **Have a rollback for code and a forward-fix for data.** Destructive down-migrations are
   often impossible; plan accordingly.

## Workflow

### 1. Classify the change

| Change | Risk | Pattern |
| --- | --- | --- |
| Add nullable column | Low | Add in one deploy; start writing when code ships |
| Add column with default | Low–medium | Metadata-only on modern PG; still brief lock |
| Add `NOT NULL` | Medium–high | Add validated check first, then set not null |
| Add index | Medium | `CONCURRENTLY` on live tables; verify validity |
| Rename column/table | High | New name + dual write + backfill + switch + drop |
| Change type | High | New column + backfill + switch reads/writes + drop |
| Drop column/table | High | Stop writing first; drop after old code is gone |
| Backfill/cleanup | High | Batched, idempotent, throttled, observable |
| Constraint | Medium | Add `NOT VALID`, validate separately |
| Partition/shard | Very high | Treat as a project, not a migration |

### 2. Map the deploy timeline

Write the sequence explicitly, including which code version runs at each step:

```
Deploy 1 (code): read both old and new columns; write old, feature-flagged.
Deploy 2 (schema): add new nullable column + index concurrently.
Deploy 3 (job): backfill new column in batches; monitor lag and errors.
Deploy 4 (code): switch reads to new column; dual write on.
Deploy 5 (code): stop writing old column; verify no reads.
Deploy 6 (schema): drop old column after the rollback window.
```

A single "migration PR" that does steps 2–6 at once is not a plan. Split it.

### 3. Bound locks and timeouts

For each DDL statement, know the lock level and set guardrails:

```sql
SET lock_timeout = '3s';
SET statement_timeout = '30s';
```

If the lock cannot be acquired quickly, fail and retry later rather than queueing behind a
long transaction and blocking every reader. Run DDL outside peak traffic when possible.

Avoid:

- `ALTER TABLE` that rewrites a large table while traffic runs.
- `CREATE INDEX` without `CONCURRENTLY` on a hot table.
- `VALIDATE CONSTRAINT` and backfill in the same transaction as a lock-heavy change.
- Long transactions that hold locks while calling external services.

### 4. Backfill safely

```sql
-- Repeat in batches, ordered by primary key, small enough to commit quickly.
WITH batch AS (
  SELECT id FROM orders
  WHERE status IS NULL
  ORDER BY id
  LIMIT 1000
  FOR UPDATE SKIP LOCKED
)
UPDATE orders o
SET status = 'pending'
FROM batch
WHERE o.id = batch.id;
```

Rules:

- Idempotent predicate (`WHERE status IS NULL`), safe to re-run.
- Batch by indexed key, not `OFFSET` (which gets slower and can skip rows).
- Sleep/throttle between batches; watch replication lag, CPU, and lock waits.
- Log progress and remaining rows; make it resumable.
- Do not run inside one giant transaction; commit per batch.
- Stop on error; do not continue past a failed batch.

### 5. Dual write / dual read when switching

When renaming or changing representation:

- Write both old and new during the transition; read the new path behind a flag.
- Compare reads (shadow read) and log mismatches before switching.
- Make the write path idempotent; retries must not duplicate or corrupt.
- Define the source of truth during the window. "Both" is not an answer.
- Keep the old path until the rollback window closes, then delete it.

### 6. Verify

Schema:

- Column exists with the right type/nullability/default.
- Index is valid and used (`pg_index.indisvalid`, `EXPLAIN`).
- Constraints are validated (`convalidated = true`).
- No unexpected locks or long-running transactions remain.

Data:

- Counts before/after; no rows lost.
- Null/blank/invalid values reduced to zero (or the accepted set).
- Application reads return correct results for old and new rows.
- Replication lag back to normal; no error spike.

Application:

- Old and new code both work against the schema (during the window).
- Rollback deploy works without another migration.
- Feature flag can disable the new path.

### 7. Rollback and cleanup

- **Code rollback:** the previous version must still work with the expanded schema.
- **Data rollback:** usually a forward fix. Keep backups/snapshots for destructive changes.
- **Cleanup:** drop old columns/indexes/triggers only after the rollback window and after
  confirming no reads/writes. Dropping is irreversible; take a backup or export first.
- **Documentation:** update schema docs, ERD, and runbooks; remove the migration flag.

## Postgres specifics

Read [references/postgres-migrations.md](references/postgres-migrations.md) before writing
DDL for PostgreSQL. It covers lock levels, `CONCURRENTLY`, `NOT VALID` constraints, type
changes, enum changes, and backfill queries.

## Gotchas

- **`CREATE INDEX CONCURRENTLY` cannot run inside a transaction.** Many migration tools wrap
  migrations in one; disable that for this statement or run it separately.
- **A failed concurrent index leaves an invalid index.** Check `pg_index.indisvalid`; drop
  and recreate rather than assuming it worked.
- **Adding a `NOT NULL` column with a default still takes a brief lock.** On older engines it
  rewrites the table; verify the version and the plan.
- **Dropping a column breaks old code immediately.** Stop writing and reading it first, then
  deploy the drop after the old version is gone.
- **Renaming is a breaking change.** Old code and clients still use the old name; use a new
  column and a transition, not `RENAME` in place.
- **Triggers can multiply write cost and deadlock.** Test them under concurrency.
- **Foreign keys and cascades can lock more than expected.** Check the referenced table.
- **Migrations on replicas lag.** A schema change may apply instantly on the primary and
  later on read replicas; the app may see a mixed state.
- **ORM auto-migrations hide destructive steps.** Review the generated SQL, not just the
  model diff.
- **Seed/fixture data can violate new constraints.** Test against a production-like dump.

## Output contract

```markdown
## Change
[Schema/data change and why.]

## Risk
[Table size, traffic, lock level, reversibility, data sensitivity.]

## Timeline
| Step | Deploy | Code behavior | Schema state | Verify | Rollback |
| --- | --- | --- | --- | --- | --- |

## DDL
```sql
-- exact statements with timeouts
```

## Backfill
[Batches, predicate, throttle, monitoring, resume plan.]

## Verification
[Queries and application checks before/after each step.]

## Rollback
[Code rollback and data forward-fix. What is irreversible?]

## Cleanup
[When old columns/indexes/flags are removed.]
```

## Quality gate

- [ ] Every step is compatible with the code version running at that moment.
- [ ] Lock levels and timeouts are known and bounded.
- [ ] Large-table index creation is concurrent (or the table is small/offline).
- [ ] Backfill is batched, idempotent, throttled, resumable, and observable.
- [ ] Destructive changes happen only after old code is gone and a backup exists.
- [ ] Old and new code both work during the transition.
- [ ] Verification covers data, schema, and application behavior.
- [ ] Rollback is possible without relying on a destructive down-migration.
