Forecast 2024 of the passenger series in three ways: plain seasonal naive,
with drift added, and multiplied by the growth rate.

In the starter code `train` (up to the end of 2023) and `test` (2024) are
ready.

**What to do:**

1. `base`: the twelve values of 2023 (`train.loc["2023"].to_numpy()`).
2. **Drift:** the slope is
   `(train.iloc[-1] - train.iloc[0]) / (len(train) - 1)`. For one year ahead
   add `slope * 12` to every month.
3. **Growth:** the rate is
   `train.loc["2023"].sum() / train.loc["2022"].sum()`. Multiply every month
   by it. Print the rate rounded to four decimals.
4. For the three forecasts print the mean absolute error and the percentage
   error (the mean of `|error| / actual`, × 100) as `name MAE percent`, one
   per line (MAE with two decimals, percent with one; order: snaive, drift,
   growth).
5. Print the skill of the growth forecast over plain seasonal naive
   (`1 - MAE_growth / MAE_snaive`), rounded to two decimals.
6. For August 2024 print the actual value and the three forecasts, rounded to
   whole numbers, on one line.

**Expected output:**

```
1.0993
snaive 40.42 10.3
drift 18.52 4.6
growth 11.11 2.8
0.73
480 448 470 492
```

The plain copy is off by 10%; with drift added it drops below 5%, and
multiplied by the growth rate below 3%. You computed the growth rate from the
training data only (2023 / 2022); using 2024 would have been leakage. From now
on the bar for this series is not plain seasonal naive but its version with
growth.
