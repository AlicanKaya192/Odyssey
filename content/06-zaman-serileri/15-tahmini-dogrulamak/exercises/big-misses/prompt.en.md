Look at the one-step error of seasonal naive on the web traffic and
measure how differently a few outlier days affect the MAE and the RMSE.

**What to do:**

1. Compute the one-step error:
   `error = (visits - visits.shift(7)).dropna()`.
2. Print the MAE, the RMSE (one decimal) and the RMSE / MAE ratio (two
   decimals) on one line.
3. Print the 6 days with the largest absolute error in `"%m-%d"` form as a
   list **in date order**.
4. Remove those 6 days and print the same three numbers again.
5. By what percentage did the MAE and the RMSE fall when the 6 days were
   removed? Print both, rounded to whole numbers, on one line.

**Expected output:**

```
307.2 728.6 2.37
['03-14', '03-21', '06-20', '06-27', '10-08', '10-15']
225.3 303.3 1.35
27 58
```

The six days belong to three events: each outlier day produces two errors,
one on its own day and one a week later (when the forecast copies that day).
6 days out of 366 change the MAE by a quarter and the RMSE by more than half.
An RMSE / MAE ratio above 2 is a warning by itself: there are a few giants
among the errors.
