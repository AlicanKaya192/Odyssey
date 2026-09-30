`date_range`, `asfreq`, `resample`, `floor` and `round` all use the same
aliases.

## Units of fixed length

| Alias | Meaning | Example |
|---|---|---|
| `s` | Second | `30s` |
| `min` | Minute | `15min` |
| `h` | Hour | `6h` |
| `D` | Calendar day | `7D` |
| `W` | Week (ending Sunday) | `W` |
| `W-MON` | Week ending Monday | `W-MON` |
| `B` | Business day (Monday–Friday) | `B` |

A number can go in front: `15min`, `6h`, `2D`, `2W`.

## Units tied to the calendar

| Alias | Meaning | First value in 2024 |
|---|---|---|
| `ME` | Month end | 31 January |
| `MS` | Month start | 1 January |
| `BME` | Last business day of the month | 31 January |
| `QE` | Quarter end | 31 March |
| `QS` | Quarter start | 1 January |
| `YE` | Year end | 31 December |
| `YS` | Year start | 1 January |

`E` is "end", `S` is "start". Months and quarters have no fixed length, so
`floor("ME")` cannot be written; these work only inside `date_range`,
`asfreq` and `resample`.

## The old names no longer work

You will see these in older tutorials and answers; current pandas raises an
error:

| Old | New |
|---|---|
| `M` | `ME` |
| `Q` | `QE` |
| `Y`, `A` | `YE` |
| `H` | `h` |
| `T` | `min` |
| `S` | `s` |
| `BM` | `BME` |

The error message: `Invalid frequency: M`. `MS`, `QS`, `YS`, `D`, `W` and `B`
did not change.

## `date_range` patterns

Two of three things: start, end, count (`periods`).

```python
pd.date_range("2024-01-01", "2024-12-31", freq="D")     # every day of the year: 366
pd.date_range("2024-01-01", periods=12, freq="MS")      # 12 month starts
pd.date_range(end="2024-12-31", periods=7, freq="D")    # the last 7 days
pd.date_range("2024-03-09", periods=24, freq="h")       # the hours of one day
pd.date_range("2024-03-04", "2024-03-29", freq="B")     # business days
pd.date_range("2024-01-01", periods=5, freq="W-MON")    # 5 Mondays
pd.date_range("2024-03-09 09:00", "2024-03-09 17:00", freq="30min")
pd.date_range("2024-03-09", periods=3, freq="D", tz="Europe/Istanbul")   # aware
```

If the start does not fit the frequency, pandas jumps to the first point that
does: `pd.date_range("2024-01-15", periods=2, freq="ME")` → 31 January,
29 February.

## How many steps?

| Data | In a day | In a week | In a year |
|---|---|---|---|
| Hourly (`h`) | 24 | 168 | 8760 (8784 in a leap year) |
| Daily (`D`) | 1 | 7 | 365 (366 in a leap year) |
| Business days (`B`) | 1 | 5 | about 261 |
| Weekly (`W`) | — | 1 | about 52 |
| Monthly (`ME`) | — | — | 12 |

These numbers come back later as the **period** of a seasonality: in hourly
data a daily pattern is 24 steps and a weekly one 168; in daily data a weekly
pattern is 7 and a yearly one 365; in monthly data a yearly pattern is 12.
