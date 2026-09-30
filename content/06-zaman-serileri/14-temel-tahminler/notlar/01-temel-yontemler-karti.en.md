## Four methods at a glance

Notation: the training data $y_1, \dots, y_T$; the horizon $h$; the length of
the season $m$.

| Method | Forecast | Good when | Weakness |
|---|---|---|---|
| Mean | The training mean | A stationary series with no trend or season | Misses the level under a trend |
| Naive | $y_T$ | A random walk: a price, an exchange rate | Ignores the season; a disaster if the last day is an outlier |
| Seasonal naive | The same position in the previous season | A strong, stable season | Follows the trend one season behind |
| Drift | $y_T + h \cdot \dfrac{y_T - y_1}{T - 1}$ | A smooth, linear trend | Looks at two points only |

## General functions

```python
import numpy as np
import pandas as pd


def future_index(train, h):
    return pd.date_range(train.index[-1], periods=h + 1, freq=train.index.freq)[1:]


def mean_forecast(train, h):
    return pd.Series(train.mean(), index=future_index(train, h))


def naive_forecast(train, h):
    return pd.Series(train.iloc[-1], index=future_index(train, h))


def seasonal_naive(train, h, m):
    last = train.iloc[-m:].to_numpy()
    return pd.Series([last[i % m] for i in range(h)], index=future_index(train, h))


def drift_forecast(train, h):
    slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
    steps = np.arange(1, h + 1)
    return pd.Series(train.iloc[-1] + slope * steps, index=future_index(train, h))
```

`train.index.freq` must be set: `asfreq("D")` or `asfreq("MS")` after reading
the file. `date_range(..., periods=h + 1)[1:]` gives the `h` dates **after**
the last training day and works for any frequency.

## Better baselines

Small corrections to the four classical methods often make a marked
difference:

| Method | Idea | Code |
|---|---|---|
| Mean of the last `k` | Naive made robust to noise | `train.iloc[-k:].mean()` |
| Mean of the last `k` seasons | Seasonal naive made robust to noise | Shape the last `k * m` values as `(k, m)`, take column means |
| Seasonal naive + drift | Season + linear trend | Add `slope * m` for every cycle |
| Seasonal naive × growth | Season + percentage growth | Multiply last season by the growth rate |
| Median | A mean robust to outlier days | `train.iloc[-k:].median()` |

The mean of the last `k` seasons:

```python
def seasonal_mean(train, h, m, k=4):
    block = train.iloc[-k * m:].to_numpy().reshape(k, m)
    pattern = block.mean(axis=0)
    return pd.Series([pattern[i % m] for i in range(h)], index=future_index(train, h))
```

Copying a single week also copies the noise of that week; the mean of four
weeks reduces the noise but reacts to a trend later.

## The one-step setup

"Forecast tomorrow every day" for the whole past:

| Method | Code |
|---|---|
| Naive | `s.shift(1)` |
| Seasonal naive | `s.shift(m)` |
| Mean of the last `k` | `s.shift(1).rolling(k).mean()` |
| Mean of the whole past | `s.shift(1).expanding().mean()` |
| Mean of the last 4 seasons | `sum(s.shift(m * i) for i in range(1, 5)) / 4` |

What they all share: the forecast does **not** include the day it forecasts.

## Which bar for which series

```text
Is there a season?
  no  -> Is there a trend / drift?
           no  -> the mean, or the mean of the last k
           yes -> naive; drift if the trend is smooth
  yes -> Is there a trend?
           no  -> seasonal naive, or the mean of the last k seasons
           yes -> seasonal naive x growth (multiplicative)
                  seasonal naive + drift (additive)
```

If unsure, compute them all and make the best one the bar: one table, a few
lines of code.

## When a baseline is enough

- When the series is very short (less than two seasons): there is no data to
  feed a complex model.
- When you forecast hundreds of series at once and cannot spend effort on
  each.
- When the decision is not sensitive to the error (a rough order quantity).
- When the skill of the complex model is below 0.05–0.10: not worth the
  maintenance.

In real forecasting competitions seasonal naive and simple exponential
smoothing have beaten a good share of far more complex methods. Do not look
down on the simple method; it has to be beaten.
