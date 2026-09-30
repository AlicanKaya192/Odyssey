In the long shape a plain `shift(1)` brings another shop's value onto a
shop's row. See the wrong and the right side by side.

**What to do:**

1. Read `stores.csv` (`parse_dates=["date"]`).
2. Add two columns: `lag_wrong = long["sales"].shift(1)` and
   `lag1 = long.groupby("store")["sales"].shift(1)`.
3. For shop B's row on 2 January 2024 print the values of `sales`,
   `lag_wrong` and `lag1` as a list.
4. Print shop B's sales on 1 January 2024 (to see that this is the right
   answer).
5. Print the correlations of `sales` with `lag_wrong` and of `sales` with
   `lag1`, rounded to three decimals, on one line.
6. Print the number of `NaN` values in the `lag1` column.

**Expected output:**

```
[190, 288.0, 180.0]
180
-0.33 0.866
4
```

The wrong lag brought A's sales of the same day instead of B's yesterday. Its
correlation is negative: the column is full, the numbers look reasonable, and
they mean nothing. In the last line there are four `NaN` values: the first
day of each shop has no yesterday.
