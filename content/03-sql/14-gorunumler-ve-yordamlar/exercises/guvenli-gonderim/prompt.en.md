Create a procedure that sets an order to `'shipped'`: `dbo.ship_order`.
Its only parameter is `@order_id` (`INT`).

The rule: if the order is not `'pending'` — or does not exist — raise
this error without updating anything:

```sql
THROW 50001, N'Order is not pending.', 1;
```

The check tries two things:

| Call | Expected |
|---|---|
| `EXEC dbo.ship_order 1001;` (already shipped) | error number `50001` |
| `EXEC dbo.ship_order 1004;` (pending) | 1004's status is `shipped` |

Putting the rule inside the procedure, rather than leaving it to whoever
calls it, means the table cannot end up in a wrong state by any route.

If you want to try what you created in the same code, put `GO` in between:
a `CREATE` has to be in a batch of its own, and a query written below it
without `GO` is a syntax error. Every run is rolled back at the end, so
you can create it again with the same name on the next run.
