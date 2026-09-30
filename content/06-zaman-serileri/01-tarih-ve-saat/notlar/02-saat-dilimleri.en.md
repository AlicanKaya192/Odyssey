## Two kinds of time

| | Naive | Aware |
|---|---|---|
| Example | `datetime(2024, 3, 9, 14, 30)` | `datetime(2024, 3, 9, 14, 30, tzinfo=ZoneInfo("Europe/Istanbul"))` |
| Knows | The wall clock | The wall clock + which zone |
| `tzinfo` | `None` | A zone |
| When | One city, no daylight saving | Different places, daylight saving, APIs |

**The two cannot be compared or subtracted:**
`TypeError: can't compare offset-naive and offset-aware datetimes`. Bring
both to the same kind first.

## `replace` versus `astimezone`

The two operations people mix up most:

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

t = datetime(2024, 3, 9, 14, 30)                 # naive

t.replace(tzinfo=timezone.utc)
# 2024-03-09 14:30+00:00   the clock STAYED, only a label was added

t.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("Europe/Istanbul"))
# 2024-03-09 17:30+03:00   the SAME moment, on another zone's clock
```

- **`replace(tzinfo=...)`**: you say "this time is already in this zone". The
  clock does not change. Use it to **declare** the zone of a naive time.
- **`astimezone(...)`**: "show this moment on another zone's clock". The clock
  changes, the moment stays. Use it to **convert**.

Giving an aware time a different zone with `replace` changes the moment; it
is almost always a bug.

## Common region names

| Name | Offset | Daylight saving |
|---|---|---|
| `UTC` | +00:00 | No |
| `Europe/Istanbul` | +03:00 | Not since 2016 |
| `Europe/London` | +00:00 / +01:00 | Yes |
| `Europe/Berlin` | +01:00 / +02:00 | Yes |
| `America/New_York` | -05:00 / -04:00 | Yes |
| `Asia/Tokyo` | +09:00 | No |

Use a **region name** rather than an offset (`+03:00`): the offset changes
with daylight saving, the region name knows the rules. If you really need a
fixed offset, use `timezone(timedelta(hours=3))`.

## Daylight saving changes (Europe/Berlin, 2024)

| Date | What happened | Result |
|---|---|---|
| 31 March 02:00 | Clocks jumped to 03:00 | 02:00–03:00 **never happened**; that day had 23 hours |
| 27 October 03:00 | Clocks went back to 02:00 | 02:00–03:00 **happened twice**; that day had 25 hours |

```python
berlin = ZoneInfo("Europe/Berlin")
datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=0).utcoffset()   # 2:00:00  the first
datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=1).utcoffset()   # 1:00:00  the second
```

The visible result in hourly data: **23 rows** on the spring day, **25 rows**
on the autumn day. A daily total counts one hour too few or too many.

## The golden rule

1. Store times in **UTC**.
2. Do the arithmetic (differences, sums, sorting) **in UTC**.
3. Convert to local time **only when showing it to a person**.
4. For a naive time from outside, **find out** its zone rather than guess;
   then declare it with `replace`.

## Unix time

```python
datetime.fromtimestamp(1710000000, tz=timezone.utc)        # seconds
datetime.fromtimestamp(1710000000123 / 1000, tz=timezone.utc)   # milliseconds
```

| Digits | Unit |
|---|---|
| 10 | Seconds |
| 13 | Milliseconds |
| 16 | Microseconds |
| 19 | Nanoseconds (pandas' internal unit) |
