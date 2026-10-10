Real records have missing days: the shop was closed, the sensor did not
work, nobody came. A calculation working row by row does **not see** the
gap: if 3 March and 6 March are two consecutive rows, a "two-day average"
actually spreads over four days.

```python
import pandas as pd

days = pd.to_datetime(["2026-03-02", "2026-03-03", "2026-03-06", "2026-03-07"])
visits = pd.Series([40, 42, 50, 47], index=days)
print(visits.rolling(2).mean().tolist())
full = visits.asfreq("D")
print(len(visits), len(full), full.isna().sum())
print(full.fillna(0).tolist())
print(full.ffill().tolist())
print(full.interpolate().round(1).tolist())
print(visits.asfreq("D", fill_value=0).rolling(2).mean().tolist())
```

```text
[nan, 41.0, 46.0, 48.5]
4 6 2
[40.0, 42.0, 0.0, 0.0, 50.0, 47.0]
[40.0, 42.0, 42.0, 42.0, 50.0, 47.0]
[40.0, 42.0, 44.7, 47.3, 50.0, 47.0]
[nan, 41.0, 21.0, 0.0, 25.0, 48.5]
```

## First make the gap visible

`asfreq("D")` fills the index so that it contains every day; the missing days
become `NaN`. 4 rows became 6: 2 days were missing. The gap is now visible;
how to fill it depends on what the data **means**:

| Method | When it is right | Here |
|---|---|---|
| `fillna(0)` | if a missing day really is zero (a closed shop) | 0, 0 |
| `ffill()` | if a value holds until the next measurement (price, stock) | 42, 42 |
| `interpolate()` | if there is a smooth transition in between (temperature) | 44.7, 47.3 |
| leave (`NaN`) | if it is unknown; let the calculation skip it | — |

## Does it matter?

In the first line the two-day average for 6 March says 46 (the average of 42
and 50); yet there were no visitors on 4 and 5 March. With the missing days
added as 0, the same average is **25**. Which is right depends on the answer
to "is a missing day zero or unknown?"; but you can only ask the question once
you see the gap.

The difference between `asfreq` and `resample`: `asfreq` only **rearranges**
(one row per day, the value as it is); `resample` **aggregates** (if more than
one value falls into a bucket, it combines them).
