Build a direct forecast for a 28-day horizon: only lags at least 28 days
old, plus the calendar. Test it on the rig of Section 15.

In the starter code `safe_features(full, calendar=True)` is ready: `lag28`,
`lag35`, `lag42`, `lag56`, two level features, day-of-week dummies and (if
`calendar=True`) a day counter, the December climb and Fourier terms. `cuts`
holds the 13 cut days.

**What to do:**

1. Write the function `forecast(train, future_index, calendar)`:
   - `full = train.reindex(train.index.union(future_index))`: the future dates
     are added as `NaN`.
   - `X = safe_features(full, calendar)`.
   - The training rows: `X.loc[train.index].dropna()`; the target is `train`
     on the same dates.
   - Fit a `LinearRegression` and return the forecast for
     `X.loc[future_index]`.
2. Run two versions over the 13 experiments: `calendar=True` and
   `calendar=False`. In each experiment the test is the 28 days after the cut.
3. For each version print the mean MAE and the worst experiment with two
   decimals as `name mean worst`, one per line (names: `with calendar`,
   `without`).
4. Print the skill of the version with the calendar over seasonal naive (17.95
   across the 13 experiments) with two decimals.

**Expected output:**

```
with calendar 10.64 16.93
without 18.98 41.35
0.41
```

The linear model with the calendar brings the error down to 10.6: neck and
neck with the ARIMA that gets the same calendar information (10.23). The
version without it is **worse** than seasonal naive. The same model, the same
data; the only difference is what you tell the model. Adding the future rows
as `NaN` and building the features in one go makes the training and
forecasting features come from the same code: when the two drift apart, the
hardest bugs to find come from there.
