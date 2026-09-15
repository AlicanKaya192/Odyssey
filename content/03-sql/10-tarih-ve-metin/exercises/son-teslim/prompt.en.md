Show each order's due date: **7 days** after the order date.

Columns: `id`, `order_date`, `due_date`. Sort by `id`.

```
id    order_date  due_date
----  ----------  ----------
1001  2026-01-08  2026-01-15
1002  2026-01-15  2026-01-22
...
```

The function for adding time to a date is `DATEADD`: it takes the unit
(`day`, `month`, `year`), the amount and the date. Writing a plain `+ 7`
on a `DATE` is an error; you have to say the unit.
