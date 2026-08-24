---
detect:
  - dep:drizzle-orm
---

# Drizzle checks

## Idiomatic

- Relational queries (`db.query.table.findMany({ with })`) for reads that need relations; the `select().from().leftJoin()` builder for aggregates and projections. Mixing both for one read is a finding.
- Schema-derived types (`typeof table.$inferSelect`, `drizzle-zod` schemas) instead of hand-written interfaces that mirror a table.
- `returning()` on inserts and updates that need the row back, instead of a second select.
- Enum columns from `pgEnum` and TypeScript unions that derive from it.

## Maintainable

- Query logic in the data layer module, not in route loaders, components, or server-function handlers.
- Column references through the table object; string column names anywhere outside `sql` fragments are findings.
- Migrations checked in alongside the schema change that needs them.

## Cognitive Load

- `and()` / `or()` trees deeper than two levels; name the sub-conditions.
- Subqueries inlined where a CTE (`db.$with`) or a named helper reads better.

## Edge Cases

- `findFirst` and `[0]` treated as present; the not-found branch is missing.
- Updates and deletes whose `where` can match zero rows with no check of the affected count when the caller assumes success.
- Unique-constraint violations on insert surfacing as a raw error instead of a domain error.
- `inArray` and `array_position` with an empty list.
- Null semantics: `eq(column, null)` never matches; `isNull` is required.
- Timestamps without timezone mode declared, compared against UTC values.

## Complexity

- N+1: a query inside a loop over rows from another query. Use `with`, a join, or `inArray` on the collected ids.
- Missing index for a column used in `where`, `orderBy`, or a join on a table that grows with user data. Check the schema file for the index.
- `select()` with no column list on wide tables when the caller uses two fields.
- Counting by loading rows (`(await findMany()).length`) instead of `count()`.

## Idempotent

- Inserts a retry would duplicate; `onConflictDoNothing` or `onConflictDoUpdate` on the natural key.
- Position or order recomputation that drifts when run twice.
- Multi-statement writes outside `db.transaction`, leaving half-applied state after a failure.

## Scalable

- `findMany` with no `limit` on tables that grow with user data.
- Offset pagination on large tables; keyset pagination on an indexed column.
- Per-row updates in a loop instead of one `update ... where inArray`.
- Whole-table reads to compute something the database can aggregate.

## Sanitization

- `sql` template fragments: every interpolated value must be a bound parameter (`${value}` or `sql.param`), never string-concatenated. `sql.raw(input)` with any user-derived input is high risk.
- Dynamic column or table names from user input; use an allow-list map to table objects.
- `orderBy` direction or column chosen from user input without an allow-list.

## Thread-safe

- Check-then-insert without a unique constraint or `onConflict`, racing two concurrent requests.
- Read-modify-write (`max(position) + 1`, balance updates) outside a transaction or without `for update`.
- Counters and sequences maintained in application code.
