## Periods

```python
p = pd.Period("2024-03", freq="M")
```

| Operation | Result |
|---|---|
| `p.start_time`, `p.end_time` | The first and last moment of the span |
| `p + 1`, `p - 1` | The next / previous period |
| `p.days_in_month` | 31 |
| `p.year`, `p.month`, `p.quarter` | 2024, 3, 1 |
| `str(p)`, `p.strftime("%b %Y")` | `2024-03`, `Mar 2024` |
| `(p - pd.Period("2023-12", "M")).n` | 3 (months apart) |
| `p.asfreq("Q")` | `2024Q1` (the quarter it belongs to) |
| `pd.Period("2024Q1").asfreq("M", how="end")` | `2024-03` |

## From dates to periods and back

```python
s.index.to_period("M")             # DatetimeIndex -> PeriodIndex
df["date"].dt.to_period("M")       # on a column
ps.to_timestamp()                  # period -> month start
ps.to_timestamp(how="end")         # period -> month end (the last moment)
ps.index.start_time                # only the starts
pd.period_range("2024-01", periods=12, freq="M")
```

## Period aliases

| Alias | Span | Example label |
|---|---|---|
| `D` | Day | `2024-03-09` |
| `W` | Week, Monday–Sunday | `2024-03-04/2024-03-10` |
| `M` | Month | `2024-03` |
| `Q` | Quarter | `2024Q1` |
| `Q-MAR` | Quarter of a fiscal year ending in March | `2024Q4` |
| `Y` | Year | `2024` |
| `h` | Hour | `2024-03-09 14:00` |

**Point aliases and span aliases differ:**

| Wanted | `date_range` / `resample` | `Period` / `to_period` |
|---|---|---|
| Month | `ME` (end), `MS` (start) | `M` |
| Quarter | `QE`, `QS` | `Q` |
| Year | `YE`, `YS` | `Y` |

## Aggregating into periods

```python
s.groupby(s.index.to_period("M")).sum()       # monthly total
s.groupby(s.index.to_period("M")).mean()      # daily mean per month
s.groupby(s.index.to_period("Q")).sum()       # quarterly
s.groupby(s.index.to_period("W")).sum()       # weekly
s.groupby([s.index.year, s.index.month]).sum()    # year and month as separate levels
```

## `Timedelta` versus `DateOffset`

| | `Timedelta` | `DateOffset` |
|---|---|---|
| Knows | A fixed duration: days, hours, minutes | The calendar: months, years, weeks, days |
| `2024-01-31` + "a month" | `days=30` → `2024-03-01` | `months=1` → `2024-02-29` |
| `2024-02-29` + "a year" | `days=365` → `2025-02-28` | `years=1` → `2025-02-28` |
| When | Measuring a duration | Moving along the calendar |

```python
t + pd.DateOffset(months=1)
t + pd.DateOffset(years=1)
t + pd.DateOffset(months=3, days=5)
t - pd.DateOffset(years=1)          # the same day last year
t + pd.DateOffset(day=1)            # the 1st of the month (singular "day": SET it)
```

The plural (`days=1`) **adds**, the singular (`day=1`) **sets** that value.
Mixing them up raises nothing; the result is simply wrong.

## Ready-made offsets

```python
from pandas.tseries.offsets import (BDay, CustomBusinessDay, MonthBegin,
                                    MonthEnd, QuarterEnd, Week, YearEnd)
```

| Offset | For `2024-03-09` (a Saturday) |
|---|---|
| `+ MonthEnd(0)` | `2024-03-31` |
| `+ MonthEnd(1)` | `2024-03-31` (the next one if already at a month end) |
| `- MonthBegin(1)` | `2024-03-01` |
| `+ MonthBegin(1)` | `2024-04-01` |
| `+ QuarterEnd(0)` | `2024-03-31` |
| `+ YearEnd(0)` | `2024-12-31` |
| `+ BDay(1)` | `2024-03-11` (Monday) |
| `+ BDay(0)` | `2024-03-11` (to the next one if not a business day) |
| `- BDay(1)` | `2024-03-08` (Friday) |

**`(0)` versus `(1)`:** `(0)` is "stay if you are already there", `(1)` is
"go to the next one in any case". Unless the date sits exactly on the
boundary, both give the same result.

## Counting business days

```python
len(pd.bdate_range("2024-03-01", "2024-03-31"))     # 21
np.busday_count("2024-03-01", "2024-04-01")         # 21  (end excluded)
np.busday_count("2024-04-01", "2024-05-01", holidays=list_of_dates)   # 18
pd.date_range(start, end, freq=CustomBusinessDay(holidays=...))
```

`np.busday_count` does **not** count the end day; `bdate_range` does.
