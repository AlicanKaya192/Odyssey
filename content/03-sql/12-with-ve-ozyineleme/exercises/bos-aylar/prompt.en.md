Show the revenue of **every month** from January 2026 to June 2026
(without the cancelled ones). Months with no orders are on the list too,
with a revenue of `0`.

Columns: `month` (the first day of the month), `revenue`. Sort by
`month`.

```
month       revenue
----------  --------
2026-01-01  32715.00
2026-02-01  28680.00
2026-03-01  7710.00
2026-04-01  30060.00
2026-05-01  0.00
2026-06-01  0.00
```

There are no orders in May and June, so those months appear in no table
— `GROUP BY` cannot bring them back by itself. Generate the months first
with a recursive `WITH`, then attach the revenue to them.
