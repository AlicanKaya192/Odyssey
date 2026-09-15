This query filters by `created_at` and also asks for `amount`:

```sql
SELECT created_at, amount FROM events
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

With an index on `created_at` alone, the server **did not use** that
index at all and read the table from start to end (150 reads): the index
has no `amount`, and going back to the table for every row was judged
more expensive than a scan.

Create a single index on `created_at` that **carries** `amount` as well.
`amount` must not be part of the key — it should not take part in the
sort order, only sit in the index. Measured: with such an index the same
query takes **3 reads**.

The check looks at the key column and the included column separately.
