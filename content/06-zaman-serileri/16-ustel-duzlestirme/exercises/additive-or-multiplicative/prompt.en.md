Forecast 2024 of the monthly passenger series with three forms of
Holt–Winters and compare them with the bar from Section 14.

In the starter code `train` (up to the end of 2023) and `test` (2024) are
ready.

**What to do:**

1. Compute the bar: the values of 2023 × (`total of 2023 / total of 2022`).
   Print its mean absolute error with two decimals.
2. Fit three models (`seasonal_periods=12`):
   - `"add-add"`: `trend="add"`, `seasonal="add"`
   - `"add-mul"`: `trend="add"`, `seasonal="mul"`
   - `"mul-mul"`: `trend="mul"`, `seasonal="mul"`
3. For each print the mean absolute error (two decimals) and the percentage
   error (one decimal) of the 12-month forecast as `name MAE percent`, one per
   line.
4. Print the skill of the best model over the bar with two decimals.
5. Print the three smoothing coefficients of the best model
   (`smoothing_level`, `smoothing_trend`, `smoothing_seasonal`) with two
   decimals as a list.
6. Print the best model's forecast for August 2024 and the actual value,
   rounded to whole numbers, on one line.

**Expected output:**

```
11.11
add-add 9.9 2.4
add-mul 8.61 2.2
mul-mul 6.53 1.7
0.41
[0.0, 0.0, 0.0]
494 480
```

All three models beat the bar; the one that fits the structure of the series
(percentage growth, a proportional season) is best. All three of its
coefficients are zero: the model never needed to change the growth rate and
the monthly factors it found at the start over 11 years. When the pattern is
this stable, all a good forecast needs is the right form.
