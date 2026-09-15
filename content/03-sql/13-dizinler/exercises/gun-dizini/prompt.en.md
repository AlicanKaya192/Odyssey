This query, which brings back one day's events, gives the right result
but reads **the whole** `events` table:

```sql
SELECT id, created_at FROM events
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

Measured: 150 reads for 58 rows — every page of the table. Create an
index on `created_at`. With the index the same query drops to **2
reads**.

There is no result table in this exercise; your `CREATE INDEX` is what
gets checked. The check does not look at the index's **name** but at its
structure: which column(s) it is built on. There should be a single
index on `events` besides the primary key.

Every run is rolled back at the end, so you can create the index again
as often as you like.
