Write the function `month_totals(orders, year)`: `orders` are
`[ISO date, total]` pairs. Insert them into the table
`orders (day TEXT, total REAL)` in memory; total the orders of the year
`year` month by month and return the dictionary `{"01": 15.5, ...}` (months
in order). Let `strftime` take the month and year in SQL.

**Expected output:**

```
{'01': 15.5, '03': 20.0}
```
