Create a view that shows the pending orders: `dbo.pending_orders`.
Columns: `id`, `customer_id`, `order_date`, `status`; only those whose
`status` is `'pending'`.

```
id    customer_id  order_date  status
----  -----------  ----------  -------
1004  3            2026-02-11  pending
1008  2            2026-03-22  pending
1010  3            2026-04-17  pending
```

One more requirement. An `UPDATE` can be written through the view, and
the change goes to the `orders` table. If someone sets an order to
`'shipped'` through the view, the order **silently disappears** from it —
measured. Your view has to **refuse** that.

The check looks at two things: the view's rows and the result of this
attempt — which is expected to be refused:

```sql
UPDATE dbo.pending_orders SET status = 'shipped' WHERE id = 1004;
```

If you want to try what you created in the same code, put `GO` in between:
a `CREATE` has to be in a batch of its own, and a query written below it
without `GO` is a syntax error. Every run is rolled back at the end, so
you can create it again with the same name on the next run.
