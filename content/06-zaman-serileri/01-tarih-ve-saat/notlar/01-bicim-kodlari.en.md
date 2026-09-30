`strptime` (read text) and `strftime` (write text) use the same codes. The
examples are for `datetime(2024, 3, 9, 14, 5, 7)`.

## Date codes

| Code | Meaning | Example |
|---|---|---|
| `%Y` | Four-digit year | `2024` |
| `%y` | Two-digit year | `24` |
| `%m` | Month, two digits | `03` |
| `%d` | Day, two digits | `09` |
| `%j` | Day of the year | `069` |
| `%B` | Month name | `March` |
| `%b` | Short month name | `Mar` |
| `%A` | Day name | `Saturday` |
| `%a` | Short day name | `Sat` |
| `%w` | Day of the week, Sunday 0 | `6` |

## Time codes

| Code | Meaning | Example |
|---|---|---|
| `%H` | Hour, 00–23 | `14` |
| `%I` | Hour, 01–12 | `02` |
| `%p` | AM / PM | `PM` |
| `%M` | Minute | `05` |
| `%S` | Second | `07` |
| `%f` | Microsecond | `000000` |
| `%z` | UTC offset | `+0300` |
| `%Z` | Zone name | `UTC` |

**Upper and lower case mean different things:** `%m` is the month, `%M` the
minute. `%y` is a two-digit year, `%Y` a four-digit one.

## Common formats

| Text | Format |
|---|---|
| `2024-03-09` | `fromisoformat` or `%Y-%m-%d` |
| `2024-03-09 14:05:07` | `fromisoformat` or `%Y-%m-%d %H:%M:%S` |
| `2024-03-09T14:05:07+03:00` | `fromisoformat` |
| `09.03.2024` | `%d.%m.%Y` |
| `09/03/2024` (Europe) | `%d/%m/%Y` |
| `03/09/2024` (US) | `%m/%d/%Y` |
| `9 March 2024` | `%d %B %Y` |
| `Mar 9, 2024` | `%b %d, %Y` |
| `20240309` | `%Y%m%d` |

## Conversions

```python
from datetime import date, datetime, timedelta, timezone

datetime.strptime("09.03.2024", "%d.%m.%Y")   # text -> datetime
datetime.fromisoformat("2024-03-09 14:05")      # ISO text -> datetime
date.fromisoformat("2024-03-09")                # ISO text -> date

dt = datetime(2024, 3, 9, 14, 5)
dt.strftime("%d.%m.%Y %H:%M")                   # datetime -> text
dt.isoformat()                                  # '2024-03-09T14:05:00'
dt.date()                                       # datetime -> date
datetime.combine(date(2024, 3, 9), dt.time())   # date + time -> datetime

datetime.fromtimestamp(1710000000, tz=timezone.utc)   # Unix seconds -> datetime
dt.replace(tzinfo=timezone.utc).timestamp()           # datetime -> Unix seconds
```

## `timedelta` reference

```python
timedelta(weeks=1, days=2, hours=3, minutes=30, seconds=15)

gap = datetime(2024, 3, 10, 6, 5) - datetime(2024, 3, 9, 22, 15)
gap.days              # 0      whole days
gap.seconds           # 28200  seconds left over after the days (0..86399)
gap.total_seconds()   # 28200.0  total seconds
gap / timedelta(hours=1)   # 7.833...  in hours
```

**`.seconds` is not the total.** For a duration of 1 day 2 hours, `.seconds`
gives only 7200 (it does not count the days). Use `total_seconds()` for the
total.

Steps that need calendar knowledge (`timedelta` cannot do them):

| Wanted | Why not | Where |
|---|---|---|
| One month later | Month lengths vary | `pd.DateOffset(months=1)`, Section 04 |
| One year later | Leap years | `pd.DateOffset(years=1)` |
| The last day of the month | The month's length | `pd.offsets.MonthEnd()` |
| The next business day | Weekends, holidays | `pd.offsets.BDay()` |
