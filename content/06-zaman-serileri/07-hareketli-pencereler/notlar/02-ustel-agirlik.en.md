## The idea

An exponentially weighted mean applies one rule at every step:

```text
new mean = alpha × today's value + (1 - alpha) × yesterday's mean
```

`alpha` is between 0 and 1: how much weight today gets. Yesterday's mean was
computed by the same rule, so the whole past is in there, but with every step
back the weight shrinks by a factor of `(1 - alpha)`.

The weights for `alpha = 0.25`:

| Days ago | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Weight | 0.250 | 0.188 | 0.141 | 0.105 | 0.079 | 0.059 | 0.044 | 0.033 |

The last 7 days carry a total weight of 0.867. The remaining 0.133 is spread
over older days: no day is ever fully forgotten, its voice is just turned
down.

## Three ways to state the weight

| Parameter | As `alpha` | How to read it |
|---|---|---|
| `alpha=0.25` | 0.25 | The weight itself |
| `span=7` | `2 / (span + 1)` = 0.25 | "Like a 7-day moving average" |
| `halflife=2.4` | `1 - 0.5 ** (1 / halflife)` | The number of steps for the weight to halve |
| `com=3` | `1 / (1 + com)` = 0.25 | The centre of mass |

All four describe the same thing; only one is given. `span` is the most
common, because it is easy to compare with a moving average.

| `span` | `alpha` | Behaviour |
|---|---|---|
| 2 | 0.667 | Very fast, almost the raw series |
| 7 | 0.250 | Balanced |
| 28 | 0.069 | Slow, very smooth |
| 365 | 0.005 | Very slow; close to the trend |

## The `adjust` parameter

```python
s.ewm(span=7).mean()                  # adjust=True (the default)
s.ewm(span=7, adjust=False).mean()    # exactly the rule above
```

- **`adjust=True`**: on the rows at the start it rescales the weights of the
  few values it has so that they sum to 1. The first values start out more
  balanced.
- **`adjust=False`**: applies the recursive rule above as it is; the first
  mean is the first value itself.

The two approach the same result as the series gets longer. The "simple
exponential smoothing" formula in textbooks is `adjust=False`.

## Compared with a moving average

| | `rolling(n).mean()` | `ewm(span=n).mean()` |
|---|---|---|
| Weights | Equal inside the window, zero outside | Fading smoothly |
| Rows at the start | `NaN` | Filled |
| Reaction to a level change | Linear until the window fills | Large at first, then slowing |
| An old outlier | Leaves the window **all at once** | Fades away slowly |
| Suppressing seasonality | **Complete** if the window equals the season | Only partial |
| Needed for the calculation | The last n values | Only the previous mean |

**The seasonality row matters.** A 7-day moving average removes the weekly
pattern completely, because the window holds exactly one of each day. `ewm`
gives the newest day more weight, so it drifts up on Saturdays and down on
Mondays. Use a moving average to clean out seasonality, and `ewm` for a
fast-reacting estimate of the level.

## Exponentially weighted volatility

```python
r = close.pct_change()
vol = r.ewm(span=20).std()
```

In an equally weighted 20-day volatility a big move sits there with the same
weight for 20 days and vanishes all at once on day 21. Exponentially weighted
volatility lets that day's effect fade gradually; that is why it is common in
risk measurement.

## A bridge to forecasting

The **last value** of a mean computed with `ewm` is one of the simplest
forecasts you can make for tomorrow: "the level is here right now". The
method is called **simple exponential smoothing**. Add a trend and it becomes
Holt; add seasonality too and it becomes Holt-Winters; all three are in
Section 16.

`alpha` means the same thing there:

- **A large `alpha`**: quick to adapt to new data, but it reacts to noise
  too.
- **A small `alpha`**: calm, but slow to notice a real change.
