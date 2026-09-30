## Putting an irregular series on a grid

```python
t = pd.read_csv("log.csv", index_col="time", parse_dates=True)["value"]

gaps = t.index.to_series().diff()
print(gaps.min(), gaps.median(), gaps.max())     # how the gaps are distributed

grid = t.resample("h").mean()                     # a regular grid
counts = t.resample("h").count()                  # records per bin
print(grid.isna().sum(), counts.min(), counts.max())
```

**How to pick the grid step:** a few times the median gap. If records arrive
about every 7 minutes, an hourly grid holds around 8 records per bin and the
mean is solid. On a 5-minute grid half the bins stay empty.

## Filling an empty bin

| Method | What it does | When |
|---|---|---|
| `ffill()` | Carries the last known value forward | A level: price, stock, a setting |
| `bfill()` | Carries the next value backward | Rarely; **it uses the future** |
| `interpolate()` | A straight line between the two ends | A slowly changing measurement: temperature |
| `interpolate(method="time")` | Interpolation proportional to time | When the index is not evenly spaced |
| `fillna(0)` | Writes zero | Only if "no record = zero" |
| None | Leaves `NaN` | The most honest when you are unsure |

A **limit** can be put on all of them:

```python
grid.ffill(limit=2)            # carry across at most 2 bins
grid.interpolate(limit=3)      # fill at most 3 bins
```

A limit leaves long outages empty. Filling a 5-hour outage with a straight
line is claiming to know what happened in those five hours.

**`bfill` and forecasting.** `bfill` fills a row with the **next** value. If
you are going to build a forecasting model this is leakage: a value unknown
at that moment is written into the past. Fine for analysis, dangerous for
modelling.

## Upsampling recipes

**Spreading a total** (monthly → daily):

```python
monthly = s.resample("MS").sum()
per_day = monthly / monthly.index.days_in_month
idx = pd.date_range(monthly.index[0], monthly.index[-1] + pd.offsets.MonthEnd(0), freq="D")
daily = per_day.reindex(idx, method="ffill")
```

The index is built by hand so that it covers all of the last month too;
`monthly.resample("D")` stops at the last label.

**Carrying a level** (weekly price → daily):

```python
daily = weekly.resample("D").ffill()
```

**Interpolating a measurement** (daily temperature → 6-hourly):

```python
six_hourly = daily.resample("6h").interpolate()
```

## The limit of upsampling

| What you have | What upsampling does **not** give you |
|---|---|
| A monthly total | The difference between days of the week |
| A daily total | The difference between hours of the day |
| A weekly price | The ups and downs within the week |

An upsampled series has more rows but **not more information.** Train a model
on it and the model learns the upsampling method itself (the straight line,
the steps), not the real pattern.

When to upsample: when two series have to be joined on the same grid (daily
sales + a monthly budget), and when the low-frequency value really does hold
for the whole period (a monthly price list, a weekly campaign).

## Daylight saving and daily bins

On a timezone-aware index `resample("D")` bins by the **local** day. The day
daylight saving starts has 23 hours, the day it ends has 25:

```python
local = utc_series.tz_convert("Europe/Berlin")
print(local.resample("D").count())     # 24, 23, 24, ...
```

The daily total comes out low on that day and high on the day it ends. When
comparing consumption, use the daily **mean** or flag those two days.
