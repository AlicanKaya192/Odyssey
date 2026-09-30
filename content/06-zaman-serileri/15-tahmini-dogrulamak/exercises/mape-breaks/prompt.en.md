`stores_long.csv` holds the 2024 sales of four shops (`date`, `store`,
`sales`). Shop C is closed on Sundays: those days have no row, which means
zero sales. Compute the error of the naive forecast for shops A and C with
three measures.

In the starter code `wide` (a date × shop table) is ready.

**What to do:**

1. Take shop A as `a` and shop C as `c`. Fill the gaps in C with zero
   (`fillna(0)`). Print how many days are zero in C.
2. Write a function `measures(y)`: the naive forecast is `y.shift(1)`; drop
   the first day (`iloc[1:]`) and return three things as a tuple: the MAE (two
   decimals), the MAPE (two decimals) and the MASE (two decimals). Let the
   denominator of MASE for this series be `(y - y.shift(7)).abs().mean()`.
3. Print the results of `measures(a)` and `measures(c)`, one per line.
4. Show that MAPE is not symmetric: print the percentage error for actual
   100 / forecast 150 and for actual 150 / forecast 100, rounded to one
   decimal, on one line.

**Expected output:**

```
52
(44.19, 13.97, 3.32)
(87.28, inf, 8.65)
50.0 33.3
```

For shop C the MAPE is `inf`: on Sundays with zero sales it divides by zero.
The MAE and the MASE are defined for both shops and can be compared. The last
line shows the second trap: the same miss of 50 units counts as 50% when the
forecast is high and 33% when it is low.
