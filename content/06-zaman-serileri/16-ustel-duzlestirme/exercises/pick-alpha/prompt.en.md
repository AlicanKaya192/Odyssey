Measure how `α` changes the one-step forecast error, then compare with the
value statsmodels finds.

`adj` is ready in the starter code: the daily sales with the weekly share
removed.

**What to do:**

1. Write the function `one_step_mae(x, alpha)`: the level is
   `x.ewm(alpha=alpha, adjust=False).mean()`; tomorrow's forecast is today's
   level, so shift the level with `shift(1)`; drop the first row and return
   the mean absolute error.
2. Print the error for `α = 0.05, 0.1, 0.2, 0.5, 1.0` with two decimals as a
   list.
3. Print the skill of the best `α` over naive (`α = 1.0`),
   `1 - MAE / MAE_naive`, with two decimals.
4. Find `α` with statsmodels:
   `ExponentialSmoothing(adj).fit().params["smoothing_level"]`; print it
   rounded to two decimals.
5. Do the same for the share price (`k`) and print the `α` found with two
   decimals. (Its index is not regular, so pass `k.to_numpy()`.)

**Expected output:**

```
[12.55, 11.46, 11.21, 11.83, 13.53]
0.17
0.2
1.0
```

For the adjusted sales the best `α` is small: the level changes slowly and
most of the daily movement is noise. For the share price `α = 1`: there is
nothing to smooth, the best forecast is the last value. The same method gives
two different diagnoses of two series.
