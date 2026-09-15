For each order, show how many days have passed since **the same
customer's** previous order. On a customer's first order the value stays
empty (`NULL`). All orders, the cancelled ones included.

Columns: `customer_id`, `id`, `order_date`, `gap_days`. Sort by
`customer_id` first, then by `order_date`.

```
customer_id  id    order_date  gap_days
-----------  ----  ----------  --------
1            1001  2026-01-08  NULL
1            1003  2026-02-02  25
1            1006  2026-03-03  29
2            1002  2026-01-15  NULL
2            1008  2026-03-22  66
...
```

The function that brings the previous row's value is `LAG`. The gap in
days is the `DATEDIFF` of the tenth section.

Careful: if all orders are put in a single line, the "previous" of 1003
becomes 1002 — another customer's order. Every customer needs a line of
their own.
