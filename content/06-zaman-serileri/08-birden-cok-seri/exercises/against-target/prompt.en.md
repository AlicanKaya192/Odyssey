Sales are daily, the target monthly (`targets.csv`: `month`, `store`,
`target`). Bring the two to the same frequency and find how much of the
target was met.

**What to do:**

1. Read the two files (`parse_dates=["date"]` for `stores.csv`).
2. Add a month column to the sales table:
   `long["date"].dt.to_period("M").astype(str)`.
3. Compute total sales per month and shop
   (`groupby(["month", "store"])["sales"].sum().reset_index()`).
4. Join with the target table on `on=["month", "store"]` and add the column
   `pct = sales / target * 100`, rounded to one decimal.
5. For June 2024 print each shop's `pct` as `shop pct`, one per line.
6. Print the number of rows where the target was met (`pct >= 100`) and the
   total number of rows on one line.
7. Print the month, shop and `pct` of the row with the lowest `pct` on one
   line.

**Expected output:**

```
A 93.2
B 92.4
C 94.4
D 89.8
27 44
2024-06 D 89.8
```

Daily sales were brought down to months; the monthly target was not copied
onto days. A target is a total: copy it onto days and every month's target
would swell by the number of days.
