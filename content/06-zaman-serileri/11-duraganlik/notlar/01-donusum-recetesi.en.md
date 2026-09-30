## From symptom to transformation

| What you see in the series | What is broken | Transformation | Code |
|---|---|---|---|
| A rising or falling level | The mean | Difference | `s.diff()` |
| A pattern tied to the calendar | The mean | Seasonal difference | `s.diff(7)`, `s.diff(12)` |
| Waves growing with the level | The variance | Logarithm | `np.log(s)` |
| A season and a slow drift | The mean | Seasonal difference + difference | `s.diff(12).diff()` |
| All of them | Both | Logarithm → seasonal difference → difference | `np.log(s).diff(12).diff()` |

Every difference costs rows at the start: `diff()` 1, `diff(12)` 12, both
together 13. `dropna()` before the test and the model.

## The way back

The model forecasts the transformed series; to read the result you undo the
transformations **in reverse order**.

| Transformation | Its inverse |
|---|---|
| `d = s.diff()` | `s = d.cumsum() + s.iloc[0]` |
| `d = s.diff(7)` | `s[t] = d[t] + s[t - 7]` (forwards from the last known week) |
| `y = np.log(s)` | `s = np.exp(y)` |
| `y = np.log(s).diff()` | `s = np.exp(y.cumsum()) * s.iloc[0]` |

For a one-step forecast the inverse is very simple:

```python
# a forecast of the difference -> level
next_level = s.iloc[-1] + predicted_change

# a forecast of the seasonal difference -> level
next_level = s.iloc[-7] + predicted_change

# a forecast of the log difference -> level
next_level = s.iloc[-1] * np.exp(predicted_log_change)
```

In Section 17 ARIMA does this way back for you; you tell it the number of
differences as `d` (plain differences) and `D` (seasonal differences). The
answer to "how many differences are needed" that you find in this section will
be exactly those two numbers.

## The log difference and the percentage change

| Real change | `pct_change()` | `np.log(s).diff()` |
|---|---|---|
| A 1% rise | 0.0100 | 0.00995 |
| A 5% rise | 0.0500 | 0.0488 |
| A 10% rise | 0.1000 | 0.0953 |
| A 50% rise | 0.5000 | 0.4055 |
| A 50% fall | −0.5000 | −0.6931 |

For small changes the two are almost the same. The log difference has two
advantages:

- **It adds up.** The sum of the daily log differences is the total log change
  of the period. Percentage changes do not add (they multiply).
- **It is symmetric.** Doubling is +0.693, halving is −0.693. In percentages:
  +100% and −50%.

The logarithm cannot be taken of a series containing zero or negative values.
With zeros, `np.log1p(s)` (that is, `log(1 + s)`) is a common fix; its inverse
is `np.expm1`.

## How many differences?

1. Plot the series. Is there a trend, a season, growing waves?
2. The logarithm, if needed.
3. With a season, a seasonal difference. Plot, look at the standard deviation.
4. If there is still a drift, a plain difference. Plot, look at the standard
   deviation.
5. If the standard deviation **rose**, undo the last step.
6. Confirm with ADF and KPSS.

In practice the number of plain differences is 0, 1, rarely 2; of seasonal
differences 0 or 1. More is almost always a mistake.

Symptoms of too many differences: the standard deviation rises; the lag-1
correlation drops to around −0.5; the series saws up and down around zero.

## Where stationarity is not required

- **Decomposition** (Section 10): it exists precisely to separate the trend
  and the season.
- **Exponential smoothing** (Section 16): it models the trend and the season
  internally.
- **Tree-based machine learning** (Section 19): stationarity is not required,
  but since trees cannot predict a level they have not seen in training,
  differencing still helps most of the time.

Where stationarity **is** required: the ARIMA family, interpreting
autocorrelation (Section 12), correlation and regression between two series.
