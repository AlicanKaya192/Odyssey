Split the daily sales into three components without a library.

**What to do:**

1. `trend`: the 7-day centred moving average.
2. `detrended = s - trend`. Average it by day of the week
   (`groupby(detrended.index.dayofweek).mean()`) and subtract its own mean so
   that it sums to zero. Call this `pattern`.
3. Print `pattern` rounded to one decimal as a list (seven numbers, Monday to
   Sunday).
4. Stretch the pattern over all the dates:
   `seasonal = pd.Series(pattern.loc[s.index.dayofweek].values, index=s.index)`.
5. `resid = s - trend - seasonal`. Print the standard deviation of the
   residual and of the series, rounded to two decimals, on one line.
6. For 12 March 2024 print the observation, trend, seasonal value and
   residual (one decimal) on one line.
7. Do the three components add back up to the series? Print the result of
   `(trend + seasonal + resid - s).abs().max() < 1e-9` on the non-`NaN` days.

**Expected output:**

```
[-42.6, -39.6, -31.1, -18.7, 19.0, 76.2, 36.7]
12.32 58.94
256 287.9 -39.6 7.8
True
```

Saturday is 76 above the trend, Monday 43 below. The standard deviation fell
from 58.94 to 12.32: most of the variability in sales is explained by the
trend and the weekly pattern.
