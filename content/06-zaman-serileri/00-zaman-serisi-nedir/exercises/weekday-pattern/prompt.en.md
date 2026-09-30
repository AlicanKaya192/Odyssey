Measure the shop's weekly seasonality. In this file each day's name is
in a ready-made column: `weekday` (`Mon`, `Tue`, ..., `Sun`).

**What to do:**

1. Read `store_sales_days.csv`.
2. Group by day of the week and take the mean of sales; sort the result from
   smallest to largest (`sort_values()`).
3. Print the highest day and its mean (one decimal).
4. Print the lowest day and its mean (one decimal).
5. Print the ratio of the highest mean to the lowest, rounded to two
   decimals.

**Expected output:**

```
Sat 336.1
Mon 217.6
1.54
```

This ratio is the first forecasting tool you have without building any
model: "next Saturday sells about one and a half times a Monday."
