All of these are used on a date column as `column.dt.<name>`. On a single
`Timestamp` the same names work without `.dt` (`t.year`).

## Parts

| Name | Gives | For `2024-03-09 14:37` |
|---|---|---|
| `year` | The year | `2024` |
| `quarter` | The quarter (1–4) | `1` |
| `month` | The month (1–12) | `3` |
| `day` | The day of the month | `9` |
| `hour`, `minute`, `second` | The parts of the time | `14`, `37`, `0` |
| `dayofweek` | The day of the week, Monday 0 | `5` |
| `dayofyear` | The day of the year | `69` |
| `day_name()` | The day's name | `Saturday` |
| `month_name()` | The month's name | `March` |
| `days_in_month` | How many days the month has | `31` |
| `date` | Only the day (a Python `date`) | `2024-03-09` |
| `time` | Only the time | `14:37:00` |

`isocalendar()` gives not a single value but a table with three columns:
`year`, `week`, `day`. Because of the year-end trap, take the two together:

```python
iso = df["date"].dt.isocalendar()
df["week_label"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
```

## Yes / no questions

| Name | Meaning |
|---|---|
| `is_month_start`, `is_month_end` | Is it the first / last day of the month |
| `is_quarter_start`, `is_quarter_end` | Is it the first / last day of the quarter |
| `is_year_start`, `is_year_end` | Is it the first / last day of the year |
| `is_leap_year` | Is it a leap year |

There is no ready-made name for weekends: `df["date"].dt.dayofweek >= 5`.

## Rounding

| Operation | What it does | For `14:37` |
|---|---|---|
| `normalize()` | Pulls the time back to midnight | `00:00` |
| `floor("h")` | Rounds down | `14:00` |
| `ceil("h")` | Rounds up | `15:00` |
| `round("15min")` | Rounds to the nearest | `14:30` |

Common units: `"D"` day, `"h"` hour, `"min"` minute, `"s"` second. Months and
years have no fixed length, so there is no `floor("M")`; for the start of the
month use `dt.to_period("M").dt.start_time` (Section 04).

## A duration column (`timedelta64`)

```python
gap = df["end"] - df["start"]

gap.dt.days                # whole days
gap.dt.total_seconds()     # total seconds
gap.dt.total_seconds() / 3600   # hours
gap / pd.Timedelta(hours=1)     # hours (the same thing)
gap > pd.Timedelta(days=3)      # comparing with a duration
```

Building a duration by hand: `pd.Timedelta("2h 15min")`,
`pd.Timedelta(days=3)`, `pd.to_timedelta(df["minutes"], unit="min")`.

## Time zone operations

| Operation | When | Does the clock change |
|---|---|---|
| `dt.tz_localize("Europe/Istanbul")` | To **declare** the zone of a naive column | No |
| `dt.tz_convert("UTC")` | To **convert** an aware column to another zone | Yes, the moment stays |
| `dt.tz_localize(None)` | To drop the zone and make it naive | No |
| `pd.to_datetime(..., utc=True)` | Straight to UTC while reading | — |

Options of `tz_localize` for daylight saving:

| Parameter | Case | Values |
|---|---|---|
| `nonexistent=` | The hour skipped in spring | `"shift_forward"`, `"shift_backward"`, `"NaT"`, `"raise"` |
| `ambiguous=` | The hour that happens twice in autumn | `"NaT"`, `"raise"`, or an array of `True`/`False` |

Getting the local day from an aware column: `dt.tz_convert(...).dt.date`.
Convert first, then take the day; the UTC day and the local day differ around
midnight.

## Turning into text

```python
df["date"].dt.strftime("%Y-%m")        # '2024-03'
df["date"].dt.strftime("%d.%m.%Y")     # '09.03.2024'
```

The result is text. For grouping, `dt.to_period("M")` is usually better: it
stays ordered and keeps behaving like a date.
