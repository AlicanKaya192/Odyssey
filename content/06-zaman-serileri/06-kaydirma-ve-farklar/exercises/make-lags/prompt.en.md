Bring yesterday's and last week's sales next to each day.

**What to do:**

1. Read `store_sales.csv` as a series `s` with a date index.
2. Build a table with three columns: `sales` (the series), `lag1`
   (`shift(1)`), `lag7` (`shift(7)`).
3. Print the number of `NaN` values in `lag1` and `lag7` on one line.
4. Print the three values on the row of 9 March 2024 as a list (`.tolist()`).
5. Print the correlation of sales with `lag1` and with `lag7`, rounded to
   three decimals, on one line.

**Expected output:**

```
1 7
[384.0, 288.0, 372.0]
0.695 0.958
```

In Section 00 you found the same two correlations by slicing the array by
hand. `shift` does the same job without losing the dates.
