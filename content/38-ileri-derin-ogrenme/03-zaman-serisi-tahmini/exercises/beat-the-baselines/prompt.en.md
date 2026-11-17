The starter trains a small LSTM on 28-day windows. At the end compute three
errors in the original units:

- `mae_lstm`: the mean absolute error between the model's test forecasts
  (turned back with `* std + mean`) and `actual`,
- `mae_naive`: the error of yesterday's value,
- `mae_week`: the error of the same day last week.

The last line compares with both.

**Expected output:**

```
True True
```
