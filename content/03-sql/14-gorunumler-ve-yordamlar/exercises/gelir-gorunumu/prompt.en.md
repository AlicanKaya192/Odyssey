Create a **view** that gives each customer's revenue over the orders that
were not cancelled: `dbo.customer_revenue`. Columns: `id`, `name`,
`revenue`.

The check reads from the view like this:

```sql
SELECT id, name, revenue FROM dbo.customer_revenue ORDER BY id;
```

```
id  name           revenue
--  -------------  --------
1   Nova Retail    4155.00
2   Bright Office  34100.00
3   Delta Systems  6710.00
4   Helix Studio   49690.00
5   Orion Labs     4510.00
```

`ORDER BY` cannot be written inside a view; the order is the job of the
query that uses the view. Naming the calculated column is required too.

If you want to try what you created in the same code, put `GO` in between:
a `CREATE` has to be in a batch of its own, and a query written below it
without `GO` is a syntax error. Every run is rolled back at the end, so
you can create it again with the same name on the next run.
