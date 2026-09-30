## Four kinds

| Kind | On the chart | Example | What to do |
|---|---|---|---|
| An isolated spike | One point up or down, normal the next day | A campaign day, an outage, a typing error | Repair or flag |
| A temporary change | A jump, then a return to normal fading over a few days | A news effect, recovery after a stock-out | Flag the stretch |
| A level shift | After some day everything is at a new level | A price change, a new branch, the measuring method changed | Not an outlier: a change point |
| A seasonal event | A jump recurring on the same date every year | A public holiday, New Year, sales week | Do not touch; a calendar variable |

The same number calls for a completely different action depending on its kind.
**Determine the kind first.**

## Detection methods

| Method | Code | Strength | Weakness |
|---|---|---|---|
| z-score | `(x - x.mean()) / x.std()` | Simple | Outliers inflate the yardstick (masking) |
| Robust z | `0.6745 * (x - med) / mad` | Not moved by extremes | Takes the season for outliers on a raw series |
| Interquartile | `q1 - 1.5 * iqr`, `q3 + 1.5 * iqr` | No distribution assumed | Useless on a trending series |
| Rolling z | A baseline from `shift(1).rolling(28)` | Adapts to the local level | Window choice; does not know the season |
| Hampel filter | Rolling median and MAD | Local and robust | Flags weekends when there is a weekly pattern |
| STL residual | `STL(..., robust=True).fit().resid` | Trend and season removed | Needs at least two seasonal cycles |

The order on a seasonal series: **robust STL → residual → robust z → sort.**

## The MAD

```python
median = x.median()
mad = (x - median).abs().median()
robust_z = 0.6745 * (x - median) / mad
```

- The median: half the data below, half above.
- The MAD: the median of the deviations from the median. It holds even if 49%
  of the data is nonsense.
- `mad == 0` can happen (when more than half the values are the same): check
  before dividing.

For normally distributed data `mad / 0.6745 ≈ std`. That is why multiplying by
0.6745 brings it to the z-score scale you know.

## The Hampel filter

A robust z in a sliding window:

```python
window = 15
med = x.rolling(window, center=True, min_periods=window // 2).median()
mad = (x - med).abs().rolling(window, center=True, min_periods=window // 2).median()
score = 0.6745 * (x - med) / mad
flagged = score.abs() > 3.5
```

It works very well on sensor data without a season. On a series with a weekly
pattern it flags every weekend; remove the pattern first.

## The threshold

| Threshold | Exceeded by chance under a normal distribution |
|---|---|
| 2 | 1 in 20 observations |
| 3 | 1 in 370 observations |
| 3.5 | 1 in 2150 observations |
| 4 | 1 in 15800 observations |

Real residuals are not normally distributed; their tails are heavy and the same
threshold flags far more days. The practical route:

1. Sort the scores from largest to smallest.
2. Look at the first 10–20: is there a natural break?
3. Compare the flagged days with the calendar: holidays, campaigns, known
   faults.
4. Note separately the days you cannot explain.

## Repair options

| Option | Code | When |
|---|---|---|
| Treat as missing and fill | `x[days] = nan`, then seasonal filling | An error or a one-off event |
| Clip | `x.clip(lower, upper)` | Many mild extremes; keep the direction, limit the size |
| Replace with the expected value | `trend + seasonal` (from STL) | A consistent, model-based repair |
| A flag column | `is_event = x.index.isin(days)` | The event is real; tell the model |
| Leave it | | A recurring event; use a robust method |

Whichever option you use: **the original series stays in a separate column**
and the list of days you touched is kept.

## Tools that resist outliers

Sometimes, instead of repairing, it is enough to choose a tool that is not
affected:

| Sensitive | Robust |
|---|---|
| Mean | Median |
| Standard deviation | MAD, interquartile range |
| `rolling().mean()` | `rolling().median()` |
| `seasonal_decompose` | `STL(..., robust=True)` |
| Mean squared error (Section 15) | Mean absolute error |

## Sometimes the outlier is the point

Fraud detection, early warning of faults, watching for cyber attacks: in these
jobs an outlier is not noise, it is **what you are looking for**. The same
tools, for the opposite purpose. Section 21 is devoted to this.
