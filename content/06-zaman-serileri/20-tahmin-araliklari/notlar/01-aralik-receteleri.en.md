## Four routes

| Route | How | Pro | Con |
|---|---|---|---|
| Empirical | The quantiles of out-of-sample errors | Assumption-free; works with any method | Needs enough past errors |
| Formula | forecast ± `z` × the standard deviation of the error | Simple | Assumes a normal distribution and zero bias |
| Model | `get_forecast(h).conf_int(alpha)` | Ready-made; widens with the horizon | Too narrow if the model is wrong |
| Quantile model | A model that learns the quantile directly | The width varies with the conditions | A separate model for each quantile |

## An empirical interval, by horizon

Keep the errors of a rolling origin horizon by horizon; take the quantile of
each horizon separately.

```python
errors = []                                   # an array of h errors per experiment
for cut in cuts:
    train = s.loc[:cut]
    test = s.loc[cut + pd.Timedelta(days=1):].iloc[:h]
    errors.append(test.to_numpy() - forecast(train, h))
errors = np.array(errors)                     # (number of experiments, h)

low = np.quantile(errors, 0.10, axis=0)       # separately for each horizon
high = np.quantile(errors, 0.90, axis=0)

point = forecast(s, h)
interval_low, interval_high = point + low, point + high
```

With few experiments, group the horizons (week by week) or pool them all;
taking a quantile from thirteen errors is unreliable.

## Widening by formula

| Method | Standard deviation of the error `h` steps ahead |
|---|---|
| Mean | `σ` (constant) |
| Naive | `σ √h` |
| Seasonal naive | `σ √(k + 1)`; `k` being the number of completed seasons |
| Drift | `σ √(h (1 + h / T))` |

`σ` is the standard deviation of the one-step error; `T` the length of the
training data. These assume the errors are independent of each other; in real
series the widening is often slower (seasonal naive on the daily sales: 17.0,
18.2, 19.5, 21.3; the formula would say 17.0, 24.0, 29.4, 33.9). **Do not
trust the formula; measure.**

## statsmodels

```python
result = fit.get_forecast(h, exog=future)     # exog: only with external variables
result.predicted_mean
result.conf_int(alpha=0.2)                    # two columns: lower, upper
result.se_mean                                # the standard error at each horizon
```

For a log model turn the ends back too:

```python
interval = np.exp(result.conf_int(alpha=0.05))
```

`ExponentialSmoothing` (Section 16) gives no interval; for it use the
empirical route, or
`statsmodels.tsa.exponential_smoothing.ets.ETSModel`.

## Measuring coverage

```python
inside = (actual >= low) & (actual <= high)
coverage = inside.mean()
width = (high - low).mean()
```

The two are read together:

| Coverage | Width | Reading |
|---|---|---|
| Close to the stated | Narrow | A good interval |
| Close to the stated | Very wide | Honest but useless |
| Below the stated | Narrow | Overconfident; the model does not know something |
| Above the stated | Wide | Overcautious; it can be narrowed |

An interval of infinite width always covers 100%. The aim is **the narrowest
interval that holds the stated coverage**.

Look at coverage period by period too: an interval whose average is right but
which always collapses in the same period (the turn of the year, in the
lesson) points to a missing variable.

## Quantiles and the pinball loss

```python
def pinball(actual, forecast, q):
    diff = actual - forecast
    return np.mean(np.maximum(q * diff, (q - 1) * diff))
```

| `q` | Penalty for forecasting low | Penalty for forecasting high |
|---|---|---|
| 0.5 | 0.5 | 0.5 |
| 0.8 | 0.8 | 0.2 |
| 0.9 | 0.9 | 0.1 |

Models that learn a quantile directly:

```python
from sklearn.ensemble import HistGradientBoostingRegressor

model = HistGradientBoostingRegressor(loss="quantile", quantile=0.9)
```

Used with the feature table of Section 19; the problem of trees not
extrapolating the level applies here too (turn the target into a difference).

## Which quantile?

$$q = \frac{c_{\text{short}}}{c_{\text{short}} + c_{\text{over}}}$$

| Case | Cost short : over | `q` |
|---|---|---|
| Fresh, cheap product; the shelf must not be empty | 4 : 1 | 0.80 |
| Expensive product that spoils quickly | 1 : 3 | 0.25 |
| Hospital supplies | 50 : 1 | 0.98 |
| Equal costs | 1 : 1 | 0.50 |

A high **service level** ("the stock should be enough 95% of the time") is
simply `q = 0.95`; its price is as much extra stock as the safety margin
added.

## When presenting

- Give two intervals: 80% (ordinary movement) and 95% (a bad day).
- Draw it as a band on the chart:
  `ax.fill_between(index, low, high, alpha=0.2)`.
- Say "interval", not "guarantee": a 95% interval is exceeded one day in
  twenty, and that is expected.
- Write next to it what the coverage has been in the past: "we said 95%; over
  the last year it held 87%."
