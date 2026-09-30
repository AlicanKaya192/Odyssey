## Which tool for which question

| What you are after | Tool | What is scored |
|---|---|---|
| Point anomaly | Robust score of the residual | A single observation |
| Contextual anomaly | The same; the expected depends on context (hour, weekday) | A single observation |
| Stuck sensor | Run length | A block |
| Flat line, frozen series | Window standard deviation near zero | A window |
| Level shift (live) | CUSUM; a run of alarms in one direction | An accumulation |
| Level shift (hindsight) | Best split and its gain | The whole series |
| Slope change | Piecewise lines; an inverted V in the single-line residual | The whole series |
| Volatility change | Ratio of the window scale to the reference | A window |

## Ways of building the "expected"

| Expected | Pro | Con |
|---|---|---|
| Median of the hour / day (a profile) | Simple, robust | Does not follow trend or a level shift |
| Median of the last `n` same days | Works live, renews itself | Treats a shift as "ordinary" within weeks |
| Seasonal naive | One line | Last week's anomaly echoes |
| STL residual (`robust=True`) | Removes trend and season together | Hindsight only; not for live use |
| Forecast model + interval (Section 20) | Knows external variables | Training is affected by anomalies |

In a live detector always `shift` for the expectation: today's value must not
enter today's expectation.

## The robust score

```python
def robust_score(resid):
    center = resid.median()
    mad = (resid - center).abs().median()
    return 0.6745 * (resid - center) / mad
```

The live version takes the scale from the past only as well:

```python
def mad(x):
    return np.median(np.abs(x - np.median(x)))


scale = 1.4826 * resid.shift(1).rolling(56, min_periods=28).apply(mad, raw=True)
score = resid / scale
```

`1.4826 × MAD` corresponds to the standard deviation under a normal
distribution (the inverse of `0.6745`).

Relative or absolute? If the noise grows with the level (sales, traffic) use
the **relative** deviation (`actual / expected − 1`); if it is constant
(temperature, pressure) the difference.

## Run length

```python
same = s.diff() == 0
block = (~same).cumsum()
length = same.groupby(block).transform("sum") + 1     # block size on every row
stuck = length >= 3
```

Raise the threshold for a series with few decimals; in a counter of whole
numbers (daily orders) repeats are ordinary and this rule is not used.

## CUSUM

```python
def cusum(z, k=1.0, h=8.0):
    up = down = 0.0
    alarms = []
    for when, value in z.items():
        up = max(0.0, up + value - k)
        down = max(0.0, down - value - k)
        if up > h or down > h:
            alarms.append((when, "up" if up > h else "down"))
            up = down = 0.0
    return alarms
```

| Setting | When raised |
|---|---|
| `k` (allowance) | Deaf to small shifts; fewer false alarms |
| `h` (threshold) | The alarm comes later; fewer false alarms |
| Clipping (`clip`) | When lowered, one-day jumps do not count |

To start: `k` half the shift you want to catch (in standard deviations); `h`
between 4 and 8. Then try it on the past.

A shift of size `d` is caught in about `h / (d − k)` steps: with `k = 1`,
`h = 8` a shift of 3 in 4 steps, a shift of 1.5 in 16.

## Best split

```python
def best_split(x, margin=14):
    x = np.asarray(x, dtype=float)
    total = ((x - x.mean()) ** 2).sum()
    best_k, best_sse = None, None
    for k in range(margin, len(x) - margin):
        left, right = x[:k], x[k:]
        sse = ((left - left.mean()) ** 2).sum()
        sse += ((right - right.mean()) ** 2).sum()
        if best_sse is None or sse < best_sse:
            best_k, best_sse = k, sse
    return best_k, 1 - best_sse / total
```

- `margin` leaves out cuts very close to the ends; a three-day "piece" is
  noise, not a change.
- Take out the season and repair the anomalies first.
- If the gain is small (0.01–0.02 in the unchanged pieces of this series) say
  there is no change.
- For a slope use the residual of `np.polyfit(t, x, 1)` instead of the mean.

For many changes there is the `ruptures` library (`Pelt`, `Binseg`); it does
not come with the app and is installed in your own environment with
`pip install ruptures`.

## Volatility

```python
def robust_sd(x):
    return 1.4826 * np.median(np.abs(x - np.median(x)))


spread = resid.rolling(72).apply(robust_sd, raw=True)
ratio = spread / spread.loc[:reference_end].median()
```

If the ratio stays above 1.5–2 the noise has changed. A plain standard
deviation misleads here: a single anomaly falling in the window inflates it.

## Choosing the threshold

| Case | Threshold |
|---|---|
| A missed event is very expensive (safety, a fault) | Low; accept false alarms |
| Every alarm takes up a person's time | High |
| There are labelled events | Draw up the precision–recall table, choose by cost |
| No labels | Sort the scores, put it where they break; count the alarms it gives on the past |

Expected false alarms = number of observations × the probability of falling
outside the threshold. On hourly data a threshold of 3 means 24 false alarms a
year; on minute data, 1400.
