This section's syntax and measurements on one page. The measurements were
made on the 20,000-row `events` table; the table's data is 150 pages.

## How it is written

```sql
-- one column
CREATE INDEX ix_events_created ON events (created_at);

-- composite: sorted by the first column, then the second
CREATE INDEX ix_events_customer_created ON events (customer_id, created_at);

-- covering: amount is not sorted, it sits in the index
CREATE INDEX ix_events_created ON events (created_at) INCLUDE (amount);

-- filtered: only the rows that meet the condition
CREATE INDEX ix_events_amount ON events (amount) WHERE amount IS NOT NULL;

-- unique
CREATE UNIQUE INDEX ux_customers_name ON customers (name);

-- dropping: the table name is required
DROP INDEX ix_events_created ON events;
```

## Seeing the indexes

```sql
SELECT name, type_desc
FROM sys.indexes
WHERE object_id = OBJECT_ID('events') AND type > 0;
```

`type > 0` leaves out the table's index-less form (a heap). Every table's
primary key shows up as `CLUSTERED`.

## Plan terms

| Term | Meaning |
|---|---|
| Clustered Index Seek | straight to the row by primary key |
| Clustered Index Scan | the whole table |
| Index Seek | straight to the place in a nonclustered index |
| Index Scan | the whole nonclustered index |
| Key Lookup | back to the table for a column the index lacks, once per row |

## Measured

| Situation | Reads |
|---|---|
| `id = 10000` | 2 |
| one day, no index | 150 |
| one day, `created_at` index | 2 |
| one day, with `YEAR`/`MONTH`/`DAY` | 42 |
| one day, with `CAST(created_at AS DATE)` | 2 |
| one day, `SELECT *` | 150 (index not used) |
| one day `created_at, amount`, with `INCLUDE (amount)` | 3 |
| 15 purchases, Index Seek + Key Lookup | 130 |
| customer 3, `(customer_id, created_at)` | 11 |
| customer 3, `(created_at, customer_id)` | 52 |
| `LIKE 'S0050%'` / `LIKE '%0050'` | 3 / 54 |
| `amount > 490`, filtered index | 2 |
| a single-row `INSERT`, no index / five indexes | 2 / 22 |

## Error messages

| Situation | Message |
|---|---|
| a unique index on a column with duplicates | `The CREATE UNIQUE INDEX statement terminated because a duplicate key was found ...` |
| adding a duplicate to a unique index | `Cannot insert duplicate key row in object ... with unique index ...` |
| a second index with the same name | `The operation failed because an index or statistics with name ... already exists on table ...` |
| dropping an index that does not exist | `Cannot drop the index ..., because it does not exist or you do not have permission.` |
| `DROP INDEX` without the table name | `Must specify the table name and index name for the DROP INDEX statement.` |
| dropping the index of a `UNIQUE` rule | `An explicit DROP INDEX is not allowed on index ... It is being used for UNIQUE KEY constraint enforcement.` |

## Measuring

```sql
SET STATISTICS IO ON;
SELECT ...;          -- in the message: Table '...'. Scan count ..., logical reads ...
SET STATISTICS IO OFF;
```

This application's result table does not show the messages; in SQL Server
Management Studio they appear on the *Messages* tab.
