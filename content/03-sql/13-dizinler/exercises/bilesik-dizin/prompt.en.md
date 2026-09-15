Create **a single two-column index** for this query:

```sql
SELECT id FROM events
WHERE customer_id = 3
  AND created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

The order of the columns matters. The column searched with equality
(`customer_id`) goes first, the one searched with a range (`created_at`)
second.

Why this order, measured:

| Query | `(customer_id, created_at)` | `(created_at, customer_id)` |
|---|---|---|
| customer 3, one day | 2 reads | 2 reads |
| customer 3 only | **11 reads** | 52 reads (a scan) |

Either one is enough for this query, but the index with `customer_id`
first also serves "all of the customer's events"; the reversed one does
not. An index can only go straight to the right place in searches where
its **first column** is known.

The check looks at the index's key columns and their order; two separate
indexes do not pass.
