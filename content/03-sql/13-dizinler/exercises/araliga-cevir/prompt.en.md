This query, which brings back the purchases (`event_type`
`'purchase'`) of June 1, 2025, gives the right result:

```sql
SELECT id, created_at, amount FROM events
WHERE event_type = N'purchase'
  AND YEAR(created_at) = 2025 AND MONTH(created_at) = 6
  AND DAY(created_at) = 1
ORDER BY created_at;
```

But even if an index is created on `created_at`, it **cannot use** it:
the column is inside a function. Measured: with the index in place this
version scanned the table (150 reads), while the range version that gives
the same result came from the index.

Write the same result without applying a function to the column.
Columns: `id`, `created_at`, `amount`; sort by `created_at`. The result
is 15 rows:

```
id    created_at           amount
----  -------------------  ------
8699  2025-06-01T00:35:00  199.99
8703  2025-06-01T02:15:00  203.99
8707  2025-06-01T03:55:00  207.99
...
```

`YEAR(`, `MONTH(` and `DAY(` are forbidden by the check.
