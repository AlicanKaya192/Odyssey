Create a **stored procedure** that brings back one customer's orders:
`dbo.customer_orders`. Its only parameter is `@customer_id` (`INT`).
Columns: `id`, `order_date`, `status`; sorted by `order_date`.

The check calls the procedure twice:

```sql
EXEC dbo.customer_orders @customer_id = 1;
EXEC dbo.customer_orders @customer_id = 4;
```

```
id    order_date  status
----  ----------  ---------
1001  2026-01-08  shipped
1003  2026-02-02  shipped
1006  2026-03-03  cancelled
```

(Two rows for customer 4: 1005 and 1009.)

Because it is called with the parameter's name, the name has to be
exactly `@customer_id`. Unlike a view, a procedure can contain an
`ORDER BY`.

If you want to try what you created in the same code, put `GO` in between:
a `CREATE` has to be in a batch of its own, and a query written below it
without `GO` is a syntax error. Every run is rolled back at the end, so
you can create it again with the same name on the next run.
