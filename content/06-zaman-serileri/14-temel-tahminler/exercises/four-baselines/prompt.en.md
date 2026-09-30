Build the four baseline forecasts, score them and save a chart.

In the starter code `train`, `test`, `h` and `future` are ready.

**What to do:**

1. Build the four forecasts as series indexed by `future`:
   - `mean_fc`: the training mean
   - `naive_fc`: the last value of the training data
   - `snaive_fc`: the last week repeated (`last_week[i % 7]`)
   - `drift_fc`: the last value + slope × step; the slope is
     `(train.iloc[-1] - train.iloc[0]) / (len(train) - 1)` and the steps are
     `np.arange(1, h + 1)`
2. Print the mean absolute error of each as `name error`, with two decimals,
   one per line (order: mean, naive, snaive, drift).
3. For the first test day (6 November) print the actual value and the four
   forecasts, rounded to whole numbers, on one line.
4. Draw a chart: the last 28 days of training and the test (grey), with the
   four forecasts on top. Save it as `chart.png`.

**Expected output:**

```
mean 75.98
naive 64.07
snaive 11.64
drift 64.6
283 255 267 286 267
```

Seasonal naive is five to six times more accurate than the other three. In the
**Output** tab on the left you will see why: the mean, naive and drift are
flat lines; only seasonal naive follows the weekly pattern.
