You have fitted a model and its error is below the bar. Three more checks
before using it.

## 1. Is any memory left in the residual?

A good model takes everything predictable; white noise is left (Section 12).

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

resid = fit.resid
print(acf(resid, nlags=14).round(2).tolist()[1:])
print(acorr_ljungbox(resid, lags=[14]))
```

| In the ACF of the residual | Meaning | What to do |
|---|---|---|
| All in the band | The model took the memory | Carry on |
| Lag 1 stands out | Short-term dependence is left | ARIMA (Section 17) |
| The seasonal lag (7, 12) stands out | The season was not fully taken | Check `seasonal` and `seasonal_periods` |
| Slowly decaying, all positive | The trend was not taken | Add `trend` |

On the Holt–Winters residual of the daily sales the Ljung–Box test still gives
a small p-value: the model takes the level and the season, not the short
memory between days. That is the natural limit of exponential smoothing.

## 2. Is the residual biased or uneven?

```python
print(round(resid.mean(), 2))                                 # should be close to zero
print(resid.abs().groupby(resid.index.year).mean().round(1))  # similar from year to year?
print(resid.abs().sort_values(ascending=False).head(5))       # the biggest misses
```

- If the mean is far from zero the model is systematically off.
- If the size of the residual grows over the years, a multiplicative season is
  needed instead of an additive one.
- If the biggest misses are always on the same dates (New Year, holidays),
  calendar information is missing.

## 3. Are the coefficients sensible?

| Case | Reading |
|---|---|
| `α ≈ 1` | The model has turned into naive; nothing to smooth |
| `α ≈ 0`, no trend | The model has turned into the mean; the series sits around a constant |
| `β ≈ 0` | The slope is constant: the initial slope is never updated |
| Large `β` | The slope changes with every surprise; dangerous at a long horizon |
| `γ ≈ 0` | The seasonal shares are fixed; close to the classical decomposition |
| Large `γ` | The seasonal shares copy the noise of the last cycle |
| `φ < 0.8` | The trend dies out very fast; the trend component may be unnecessary |

A coefficient sticking to a boundary (0 or 1) is not an error; it is a
finding. But on a short series a coefficient at the boundary usually means
"not enough data".

## Training error and test error

```python
train_mae = fit.resid.abs().mean()
test_mae = (test - fit.forecast(len(test))).abs().mean()
```

The test error is naturally larger: the training error is **one-step**, the
test error **multi-step**. But if the test error is many times the training
error, the model has memorised, or the test period is in a different regime
from the training.

For the passenger model the training error is 2.6 and the test error 6.5:
reasonable. For the sales model with a multiplicative season, getting 8.9 on
the single split and 15.5 across 13 experiments was a warning: the single
split was optimistic.

## Which model for which series

```text
Is there a season?
  no  -> Is there a trend?
           no  -> simple exponential smoothing
           yes -> Holt; damped at a long horizon
  yes -> Do the waves grow with the level?
           no  -> seasonal="add"
           yes -> seasonal="mul"
         Is there a trend?
           unsure -> compare the two candidates, with and without, on a rolling origin
```

For every decision you are unsure of, put the two candidates through the rig
of Section 15. If they tie, choose the one with **fewer components**: easier
to maintain, with a better worst case.

## In production

- The model is **refitted**: as new data arrives (daily or weekly), `fit` from
  scratch. Exponential smoothing is fast; this is not a problem.
- For final use, fit on **all the data**, validation and test included.
- Store the baseline forecast alongside the forecast; if the model
  deteriorates (skill drops below zero) that is where it shows first.
- Repair outlier days before fitting (Section 13): with a large `α` a single
  spike keeps the level up for days.
