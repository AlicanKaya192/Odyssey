# datetime

How many days ago an order was placed, when a subscription ends, what time a
meeting is in New York, which day the text `05/03/2026` in a file means...
Every job with dates and times is done with the **`datetime`** module. In this
section we build date objects, compute the difference between them (a
duration), turn them into text and read them from text, and look at time
zones.

## Three objects: date, time, datetime

```python
from datetime import date, time, datetime

d = date(2026, 3, 15)
t = time(14, 30)
dt = datetime(2026, 3, 15, 14, 30)
print(d, t, dt)
print(dt.year, dt.month, dt.day, dt.hour, dt.minute)
print(d.weekday(), d.isoweekday(), d.strftime("%A"))
print(datetime.combine(d, t) == dt, dt.date() == d)
```

```text
2026-03-15 14:30:00 2026-03-15 14:30:00
2026 3 15 14 30
6 7 Sunday
True True
```

- **`date`** is only a day (year, month, day), **`time`** only a clock time,
  **`datetime`** both.
- The parts are read as attributes: `dt.year`, `dt.hour`...
- `weekday()` counts Monday as 0, `isoweekday()` as 1. 15 March 2026 is a
  Sunday: 6 and 7.
- `datetime.combine(day, time)` joins the two, `dt.date()` takes the day out.

Today's date is `date.today()`, the current moment `datetime.now()`. Because
they give a different result on every run, the examples in this section use
fixed dates; in the exercises too the date always comes in as a parameter.

## Durations: timedelta

The difference of two dates is a **`timedelta`** (duration) object; durations
can be added to and subtracted from dates.

```python
from datetime import date, datetime, timedelta

start = date(2026, 3, 15)
print(start + timedelta(days=30))
print(date(2026, 12, 31) - start)
gap = datetime(2026, 3, 16, 9, 0) - datetime(2026, 3, 15, 14, 30)
print(gap, gap.days, gap.seconds, gap.total_seconds())
print(timedelta(weeks=2, hours=36))
print(date(2026, 3, 15) < date(2026, 4, 1))
```

```text
2026-04-14
291 days, 0:00:00
18:30:00 0 66600 66600.0
15 days, 12:00:00
True
```

30 days after 15 March is 14 April; there are 291 days to the end of the
year. Between 14:30 yesterday and 09:00 today there are 18.5 hours:
`gap.days` is 0, `gap.seconds` 66,600. Careful: `seconds` does **not**
include the day part; when you need the whole duration always use
**`total_seconds()`**. Dates are compared with `<`, `>`, `==` and sorted with
`sorted`.

`timedelta` has `days`, `weeks`, `hours`, `minutes`, `seconds` parameters but
**no `months` or `years`**: months have different lengths, so "one month
later" is not a fixed duration. Adding months is in the second note.

## To text and from text

```python
from datetime import datetime

dt = datetime(2026, 3, 5, 9, 7)
print(dt.strftime("%d.%m.%Y %H:%M"))
print(dt.strftime("%Y-%m-%d"), dt.isoformat())
parsed = datetime.strptime("05/03/2026 09:07", "%d/%m/%Y %H:%M")
print(parsed == dt)
print(datetime.fromisoformat("2026-03-05T09:07:00"))
```

```text
05.03.2026 09:07
2026-03-05 2026-03-05T09:07:00
True
2026-03-05 09:07:00
```

- **`strftime`** (string **f**ormat **time**): date → text.
- **`strptime`** (string **p**arse **time**): text → date; the format must
  match the text exactly.
- **`isoformat` / `fromisoformat`**: the international `YYYY-MM-DD` format.
  Use it for storing data and in file names: sorted as text it is also in
  date order.

The most used format codes:

| Code | Meaning | Example |
|---|---|---|
| `%Y` | four-digit year | 2026 |
| `%m` | month (01–12) | 03 |
| `%d` | day (01–31) | 05 |
| `%H` | hour (00–23) | 09 |
| `%M` | minute (00–59) | 07 |
| `%S` | second | 00 |
| `%A` / `%a` | day name / short | Thursday / Thu |
| `%B` / `%b` | month name / short | March / Mar |

Lowercase `%m` is the **month**, uppercase `%M` the **minute**; mixing them
up is the most common mistake. Day and month names can change with the
system's language setting; if the program must behave the same everywhere,
take the names from your own list (`["Mon", "Tue", ...][d.weekday()]`).

## Time zones

The `datetime` objects so far are **naive**: they do not know which time zone
they are in. An object given a `tzinfo` becomes **aware**. Time zones are
taken from the `zoneinfo` module by their `"Region/City"` name.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

meeting = datetime(2026, 3, 15, 14, 30, tzinfo=ZoneInfo("Europe/Istanbul"))
print(meeting)
print(meeting.astimezone(ZoneInfo("America/New_York")))
print(meeting.astimezone(timezone.utc))
summer = datetime(2026, 7, 15, 12, 0, tzinfo=ZoneInfo("Europe/London"))
winter = datetime(2026, 1, 15, 12, 0, tzinfo=ZoneInfo("Europe/London"))
print(summer.utcoffset(), winter.utcoffset())
```

```text
2026-03-15 14:30:00+03:00
2026-03-15 07:30:00-04:00
2026-03-15 11:30:00+00:00
1:00:00 0:00:00
```

A meeting at 14:30 in Istanbul is at 07:30 in New York and 11:30 in UTC.
**`astimezone`** shows the same moment on another clock. London is UTC+1 in
summer and UTC+0 in winter: because of **daylight saving time** the
difference changes during the year. That is why writing the difference by
hand (`+ timedelta(hours=3)`) is wrong; `ZoneInfo` knows which difference
applies on which date.

A common rule is to store time as **UTC** on servers and in databases and to
convert it to the user's time zone when showing it.

## Common mistakes

```python
from datetime import date, datetime
from zoneinfo import ZoneInfo

naive = datetime(2026, 3, 15, 14, 30)
aware = datetime(2026, 3, 15, 14, 30, tzinfo=ZoneInfo("Europe/Istanbul"))
try:
    print(aware - naive)
except TypeError as error:
    print("TypeError:", error)
try:
    datetime.strptime("2026-13-01", "%Y-%m-%d")
except ValueError as error:
    print("ValueError:", error)
try:
    date(2026, 1, 31).replace(month=2)
except ValueError as error:
    print("ValueError:", error)
print(datetime.strptime("09:07", "%H:%m"))
```

```text
TypeError: can't subtract offset-naive and offset-aware datetimes
ValueError: time data '2026-13-01' does not match format '%Y-%m-%d'
ValueError: day 31 must be in range 1..28 for month 2 in year 2026
1900-07-01 09:00:00
```

- Naive and aware objects cannot be subtracted or compared.
- There is no 13th month: `strptime` raises `ValueError` for text that does
  not fit the format. Dates read from a file need to be read inside `try`.
- Setting the month of 31 January to 2 asks for 31 February; that day does
  not exist.
- With `"%H:%m"`, 07 was read as the **month**: the result is July of the
  year 1900. Because it raises no error, this is the sneakiest one.

## Summary

- `date` is a day, `time` a clock time, `datetime` both; the parts are read
  with attributes like `year`, `month`, `hour`.
- The difference of two dates is a `timedelta`; the whole duration is
  `total_seconds()`. Months and years are not in `timedelta`.
- `strftime` date → text, `strptime` text → date; `%m` month, `%M` minute.
- Store in ISO format (`isoformat`, `fromisoformat`).
- A time zone is `ZoneInfo("Europe/Istanbul")`; converting is `astimezone`.
  Do not write the difference by hand, daylight saving time changes it.
