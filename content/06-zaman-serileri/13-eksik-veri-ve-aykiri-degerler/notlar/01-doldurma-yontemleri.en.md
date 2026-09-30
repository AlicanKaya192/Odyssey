## Checklist

```python
raw["date"].is_monotonic_increasing        # in order?
raw["date"].duplicated().sum()             # the same date more than once?
raw["sales"].isna().sum()                  # explicit gaps
(raw["sales"] <= 0).sum()                  # may be gaps in disguise

full = raw.groupby("date")["sales"].sum().asfreq("D")
full.isna().sum()                          # the real number of gaps
full.isna().mean()                         # the share missing
```

Work out the expected number of rows yourself and compare:
`len(pd.date_range(start, end, freq="D"))`.

## The methods

| Method | Code | When | Risk |
|---|---|---|---|
| Zero | `fillna(0)` | Missing = really zero (a closed day) | Counting the unknown as zero |
| Last value | `ffill()` | Valid until the value changes (price, stock, status) | Erases the season; stale over a long gap |
| Next value | `bfill()` | Only when filling the start of a series | Uses the future |
| Linear | `interpolate()` | A slowly, smoothly changing measurement (temperature) | Erases the season; uses the future |
| By time | `interpolate(method="time")` | An irregularly spaced index | The same |
| Last season | `fillna(s.shift(m))` | A seasonal series | A little low if there is a trend |
| Mean of two seasons | The mean of `shift(m)` and `shift(-m)` | A seasonal series, when cleaning the past | Uses the future |
| Mean of the seasonal position | `groupby(...).transform("mean")` | A seasonal series without a trend | Ignores the trend |
| Rolling median | `fillna(s.rolling(7, center=True, min_periods=1).median())` | Noisy, no season | Uses the future |
| A model | With STL / ARIMA | Long or many gaps | Complex; overconfidence |

By default `interpolate()` treats the rows as **evenly spaced**. With an
irregular index, `method="time"` uses the real time difference.

## `limit` and the short-gap pattern

```python
s.ffill(limit=2)                     # at most 2 cells of each gap
s.interpolate(limit=3)               # the same; fills the first 3 of a long gap too
s.interpolate(limit_area="inside")   # only between two defined values
```

"Fill only gaps of `n` or shorter":

```python
missing = s.isna()
run_id = (missing != missing.shift()).cumsum()
run_length = missing.groupby(run_id).transform("sum")

short = missing & (run_length <= n)
result = s.where(~short, s.interpolate())
```

## Backward-looking and forward-looking

| Backward-looking (no leakage) | Looking both ways (uses the future) |
|---|---|
| `ffill()` | `bfill()` |
| `fillna(s.shift(m))` | `interpolate()` |
| A trailing `rolling(...).mean()` | `center=True` windows |
| | Anything with `shift(-m)` |

When cleaning a report on the past, looking both ways is allowed and more
accurate. When testing a forecasting model (Section 15), the left column only.

## Totals and means

`sum()` and `mean()` **skip** `NaN`. As a result:

- The **total** of a month with missing days comes out low (as if the missing
  days counted as zero).
- The **mean** is computed from the available days only; if the missing days
  are not random (always Sundays), it is biased.

To leave a period with missing days empty when resampling:

```python
monthly = full.resample("MS").sum(min_count=28)
```

`min_count`: if the period has fewer defined values than this, the result is
`NaN`.

## Flagging

```python
frame = pd.DataFrame({
    "sales": filled,
    "was_missing": full.isna(),
})

frame["was_missing"].groupby(frame.index.month).sum()     # filled per month
frame.loc[~frame["was_missing"], "sales"].mean()          # real days only
```

In a machine learning model (Section 19) `was_missing` can also be given as a
feature: the missingness itself may carry information.

## When not to fill

- When the gap is longer than the season and you only have one or two cycles
  of data.
- When more than 5–10% of the data is missing.
- When what is missing is the **target** you are trying to forecast and you
  will evaluate the model over that period.
- When the cause of the gap is unknown: find the cause first.

In these cases the options are: leave the gap and use a method that accepts it
(the state space models of statsmodels handle `NaN` themselves), move to a
coarser frequency, or start the series after the gap.
