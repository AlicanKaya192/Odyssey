Create a procedure that returns a customer's number of orders through an
**output parameter**: `dbo.customer_order_count`. Parameters, in this
order:

| Parameter | Type | Its job |
|---|---|---|
| `@customer_id` | `INT` | which customer |
| `@order_count` | `INT` | **output**: the number is written here |
| `@status` | `NVARCHAR(20)` | optional; if not given, every status |

The procedure returns no result table; the number comes back only
through `@order_count`. The check calls it like this:

```sql
DECLARE @all INT, @shipped INT, @none INT;
EXEC dbo.customer_order_count 1, @all OUTPUT;
EXEC dbo.customer_order_count @customer_id = 1, @order_count = @shipped OUTPUT,
                              @status = N'shipped';
EXEC dbo.customer_order_count 6, @none OUTPUT;
SELECT @all, @shipped, @none;   -- expected: 3, 2, 0
```

The caller has to write `OUTPUT` too. Without it the variable stays
`NULL` and **no error comes back either** (measured).

If you want to try what you created in the same code, put `GO` in between:
a `CREATE` has to be in a batch of its own, and a query written below it
without `GO` is a syntax error. Every run is rolled back at the end, so
you can create it again with the same name on the next run.
