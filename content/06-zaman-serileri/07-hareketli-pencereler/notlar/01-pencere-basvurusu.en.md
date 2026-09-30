## Three kinds of window

| Window | What it looks at | Written as |
|---|---|---|
| Rolling | The last n rows (or the last n days) | `s.rolling(7)`, `s.rolling("7D")` |
| Expanding | Everything from the start until today | `s.expanding()` |
| Exponentially weighted | Everything, with newer values weighing more | `s.ewm(span=7)` |

All three are followed by an operation: `.mean()`, `.sum()`, `.std()`...

## `rolling` parameters

| Parameter | What it does |
|---|---|
| `window=7` | The window length, in **rows** |
| `window="7D"` | The window length, in **time** (needs a date index) |
| `min_periods=1` | Give a result if the window holds at least this many values |
| `center=True` | Put the window on both sides of the row (uses the future) |
| `closed="left"` | In a time window, leave today out |

The default `min_periods`: the window length for a row window (hence the
`NaN` at the start), 1 for a time window (the start is filled but with few
observations).

## Operations

| Operation | Gives |
|---|---|
| `mean()` | A moving average: smoothing |
| `sum()` | A moving total: "sales of the last 7 days" |
| `std()`, `var()` | Rolling volatility |
| `min()`, `max()` | The lowest / highest in the window |
| `median()` | Smoothing that is robust to outliers |
| `quantile(0.9)` | The window's 90th percentile |
| `count()` | How many valid values the window holds |
| `corr(other)` | The rolling correlation of two series |
| `apply(function)` | Your own calculation (slow) |

```python
s.rolling(7).apply(lambda x: x.max() - x.min())     # the range of the window
s.rolling(90).corr(other)                           # does the link change over time
```

## Window length

| Data | Pattern to suppress | Window |
|---|---|---|
| Hourly | Daily | 24 |
| Hourly | Weekly | 168 |
| Daily | Weekly | 7 |
| Daily | Yearly | 365 |
| Business days | Weekly | 5 |
| Monthly | Yearly | 12 |
| Quarterly | Yearly | 4 |

**Even windows and centring.** A centred 12-month window has no exact middle
(it falls between months 6 and 7). The classic fix is to take a 12-term mean
and then a 2-term mean of that (a 2×12 moving average); the window then sits
squarely on a month. The decomposition in Section 10 does this itself.

## Delay

A trailing mean of n shows how things were about **(n - 1) / 2** steps ago:

| Window | Delay |
|---|---|
| 7 | 3 days |
| 28 | 13–14 days |
| 365 | about 6 months |

As the window grows, the series gets calmer **and** turning points are seen
later. No window improves both; it is a trade-off.

## Building features

```python
past = s.shift(1)                          # from yesterday backwards

features = pd.DataFrame({
    "mean_7": past.rolling(7).mean(),
    "mean_28": past.rolling(28).mean(),
    "std_7": past.rolling(7).std(),
    "max_7": past.rolling(7).max(),
    "ewm_7": past.ewm(span=7).mean(),
})
```

Every window is built after `shift(1)`. If you forecast h steps ahead, use
`shift(h)`: the latest value known when you forecast is the one h steps
earlier.

## Is it safe? A quick check

| Expression | Does it use the future |
|---|---|
| `s.rolling(7).mean()` | No, but it contains **today** |
| `s.shift(1).rolling(7).mean()` | No |
| `s.rolling(7, center=True).mean()` | **Yes**: 3 days ahead |
| `s.expanding().mean()` | No; it contains today |
| `s.ewm(span=7).mean()` | No; it contains today |
| `s.rolling(7).mean().shift(-3)` | **Yes**: the same as a centred window |
| `(s - s.mean()) / s.std()` | **Yes**: the mean of the whole series contains the future |

The last row slips through a lot: scaling with the mean and standard
deviation of the whole series leaks future values onto today's row. Use a
mean computed with `expanding` or `rolling` instead.

## On series with gaps and irregular series

```python
s.rolling("7D").mean()                   # mean of the last 7 days, however many records
s.rolling("7D").count()                  # how many records are in that window
s.rolling("7D", min_periods=7).mean()    # NaN unless there are 7 records
s.rolling("24h").mean()                  # the last 24 hours, in hourly / irregular data
```

A time window cannot be used with `center=True`, and the index has to be
sorted.
