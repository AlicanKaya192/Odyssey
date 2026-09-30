# Dates and Times in Python

In the previous section dates were text: `"2022-01-01"`. We could sort them
as text and take the year from the first four characters. But text cannot
answer any of these questions:

- How many days are there between 27 February and 4 March?
- Which day of the week is 9 March 2024?
- A 7 hour 50 minute shift starts at 22:15; when does it end?

The answers depend on the calendar: months have different lengths, some years
have 366 days, a duration that crosses midnight rolls into the next day. You
need a **type** that knows these things. In Python it comes from the
`datetime` module of the standard library, and every date in pandas is built
on the same idea. Learn this section well and you already know half of the
next ones.

## Four types

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>date</code></span><span>Only the day: <code>date(2024, 3, 9)</code></span></div>
    <div class="anat-row"><span><code>time</code></span><span>Only the clock time: <code>time(14, 30)</code>; rarely used on its own</span></div>
    <div class="anat-row"><span><code>datetime</code></span><span>Day and time together: <code>datetime(2024, 3, 9, 14, 30)</code></span></div>
    <div class="anat-row"><span><code>timedelta</code></span><span>Not a <b>moment</b> but a <b>duration</b>: <code>timedelta(days=6)</code></span></div>
  </div>
  <figcaption>The first three describe a point on the calendar, the last one the distance between two points.</figcaption>
</figure>

```python
from datetime import date, datetime, time, timedelta

d = date(2024, 3, 9)
t = datetime(2024, 3, 9, 14, 30)

print(d)               # 2024-03-09
print(t)               # 2024-03-09 14:30:00
print(d.year, d.month, d.day)      # 2024 3 9
print(t.hour, t.minute)            # 14 30
```

The order is always from largest to smallest: **year, month, day, hour,
minute, second.** Write `date(9, 3, 2024)` and Python looks for day 2024 of
month 3 of the year 9, and raises an error.

**An invalid date cannot be built.** This is the biggest gain over text:

```python
date(2023, 2, 29)
# ValueError: day 29 must be in range 1..28 for month 2 in year 2023
```

2023 is not a leap year; February has 28 days. A text like `"2023-02-29"` can
be typed freely and sit unnoticed in a table; `date` does not allow it.

## Day of the week

```python
d = date(2024, 3, 9)
print(d.weekday())      # 5   (Monday 0 ... Sunday 6)
print(d.isoweekday())   # 6   (Monday 1 ... Sunday 7)
```

There are two numberings and both are common. **`weekday()` starts at
zero**, `isoweekday()` at one. `d.weekday() >= 5` is the shortest way to pick
weekends. pandas follows the same rule: `dayofweek` is 0 for Monday.

## Durations: `timedelta`

The difference between two dates is a **duration**, and a duration is a type
of its own.

```python
order = date(2024, 2, 27)
delivery = date(2024, 3, 4)

gap = delivery - order
print(gap)          # 6 days, 0:00:00
print(gap.days)     # 6
```

The same two dates are 5 days apart in 2023: in 2024, 29 February sits in
between. Counting the calendar by hand, this is very easy to miss.

A duration can also be built by hand and added to a date:

```python
start = datetime(2024, 3, 9, 22, 15)
end = start + timedelta(hours=7, minutes=50)

print(end)                             # 2024-03-10 06:05:00
print((end - start).total_seconds())   # 28200.0
```

It crossed midnight, and the date rolled over to the next day on its own.

<figure class="fig">
  <div class="flow">
    <span class="node"><code>datetime</code></span><span class="arrow">−</span>
    <span class="node"><code>datetime</code></span><span class="arrow">=</span>
    <span class="node acc"><code>timedelta</code></span>
  </div>
  <div class="flow">
    <span class="node"><code>datetime</code></span><span class="arrow">+</span>
    <span class="node acc"><code>timedelta</code></span><span class="arrow">=</span>
    <span class="node"><code>datetime</code></span>
  </div>
  <figcaption>The difference of two moments is a duration; a moment plus a duration is a new moment. Adding two moments makes no sense: <code>datetime + datetime</code> raises an error.</figcaption>
</figure>

**`timedelta` knows no months or years.** There is no `timedelta(months=1)`,
because "a month" is not a fixed duration: 31 days in January, 28 or 29 in
February. Approximating with days goes wrong:

```python
date(2024, 1, 31) + timedelta(days=30)    # 2024-03-01  (not "a month later")
date(2024, 2, 29) + timedelta(days=365)   # 2025-02-28  (not "a year later")
```

"One month later" by the calendar is done with pandas' `DateOffset`; that is
Section 04.

## Comparing and sorting

Dates compare like numbers; `min`, `max` and `sorted` work correctly:

```python
days = [date(2024, 3, 9), date(2023, 1, 10), date(2024, 12, 1)]
print(sorted(days))    # [2023-01-10, 2024-03-09, 2024-12-01]
print(max(days))       # 2024-12-01
```

If the same three dates were day-first text:

```python
sorted(["09.03.2024", "10.01.2023", "01.12.2024"])
# ['01.12.2024', '09.03.2024', '10.01.2023']   wrong
```

Text is compared left to right, so only the days were compared. The fix is to
turn the text into dates.

## From text to date: `strptime`

A date coming from a file, a user or another system is almost always text. To
convert it you have to state the **format**:

```python
datetime.strptime("09.03.2024", "%d.%m.%Y")          # 2024-03-09 00:00:00
datetime.strptime("03/09/2024", "%m/%d/%Y")          # 2024-03-09 00:00:00
datetime.strptime("9 March 2024 14:30", "%d %B %Y %H:%M")
```

`%d` is the day, `%m` the month, `%Y` the four-digit year. Everything else in
the format (dots, slashes, spaces) must match the text exactly.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>%d</code> → <code>09</code></span><span>Day, two digits</span></div>
    <div class="anat-row"><span><code>%m</code> → <code>03</code></span><span>Month, two digits (lower-case m)</span></div>
    <div class="anat-row"><span><code>%Y</code> → <code>2024</code></span><span>Four-digit year (upper-case Y; <code>%y</code> is two digits)</span></div>
    <div class="anat-row"><span><code>%H</code> → <code>14</code></span><span>Hour, 00–23</span></div>
    <div class="anat-row"><span><code>%M</code> → <code>30</code></span><span>Minute (upper-case M)</span></div>
  </div>
  <figcaption>The format of the text <code>"09.03.2024 14:30"</code> is <code>"%d.%m.%Y %H:%M"</code>. The full list of codes is in the "Format Codes" note.</figcaption>
</figure>

**`03/09/2024` on its own is ambiguous.** In the US it is 9 March, in Europe
3 September. There is no way to tell from the text; you need to know who
produced the data. Mix up `%d/%m` and `%m/%d` and for days up to the 12th it
**does not even raise an error**, it silently produces the wrong date. Look
for a row with a day above 12 (`13/09/2024`) and you know which format it is.

ISO 8601 text needs no format:

```python
datetime.fromisoformat("2024-03-09 14:30")
date.fromisoformat("2024-03-09")
```

## From date to text: `strftime`

The other direction uses the same codes:

```python
d = date(2024, 3, 9)
print(d.strftime("%d.%m.%Y"))       # 09.03.2024
print(d.strftime("%A, %d %B"))      # Saturday, 09 March
print(d.isoformat())                # 2024-03-09
```

To keep the two names apart: **`strptime` = parse** (read the text),
**`strftime` = format** (write the text).

`%A` and `%B` give day and month names. These names can change with the
computer's regional settings; never store a date with names in it, use
`isoformat()`.

## ISO week number

The standard answer to "which week of the year?" is the ISO week: weeks start
on Monday and the week **containing the year's first Thursday** is week 1.

```python
for d in [date(2024, 12, 29), date(2024, 12, 30), date(2025, 1, 1)]:
    print(d, d.isocalendar())
```

```text
2024-12-29 (year=2024, week=52, weekday=7)
2024-12-30 (year=2025, week=1, weekday=1)
2025-01-01 (year=2025, week=1, weekday=3)
```

**30 December 2024 is week 1 of 2025.** It happens the other way too:
1 January 2021 is week 53 of 2020. If a weekly report takes the year from
`d.year` and the week from `isocalendar()`, at the turn of the year you get a
week that does not exist, such as "week 1 of 2024". **Take the year from
`isocalendar()` along with the week.**

## Time zones

Every `datetime` so far has been **naive**: it says `14:30` but does not know
where that 14:30 is. That is fine while you work in one city. When data comes
from different places, or from a place with daylight saving time, you need an
**aware** time that carries its zone.

```python
from datetime import timezone
from zoneinfo import ZoneInfo

berlin = ZoneInfo("Europe/Berlin")
meeting = datetime(2024, 3, 31, 9, 0, tzinfo=berlin)

print(meeting.astimezone(timezone.utc))                    # 2024-03-31 07:00:00+00:00
print(meeting.astimezone(ZoneInfo("Europe/Istanbul")))     # 2024-03-31 10:00:00+03:00
```

`ZoneInfo` takes a region name (`"Europe/Berlin"`, `"America/New_York"`) and
knows that region's daylight saving rules. **UTC** is nobody's local time; it
has no daylight saving and never shifts. That is why it is the common
language.

**The daylight saving trap.** Berlin moved its clocks one hour forward on the
night of 31 March 2024. A meeting at the same time one day earlier lands on a
different time in Istanbul:

```text
2024-03-30 09:00 Berlin  ->  11:00 Istanbul   (Berlin UTC+1)
2024-03-31 09:00 Berlin  ->  10:00 Istanbul   (Berlin UTC+2)
```

Istanbul has not used daylight saving since 2016; it is always UTC+3. The gap
changes twice a year.

The sneakier part is duration arithmetic:

```python
a = datetime(2024, 3, 30, 12, 0, tzinfo=berlin)
b = datetime(2024, 3, 31, 12, 0, tzinfo=berlin)

print(b - a)                                                 # 1 day, 0:00:00
print(b.astimezone(timezone.utc) - a.astimezone(timezone.utc))   # 23:00:00
```

Subtract two times in the same zone and Python looks at the **wall clock**:
12:00 to 12:00 is "1 day". In reality **23 hours** passed; one hour that
night never happened. When you sum hourly consumption or compute a machine's
running time, that difference is simply a wrong result.

<figure class="fig">
  <svg viewBox="0 0 680 170" width="680" xmlns="http://www.w3.org/2000/svg"><text class="ink" x="16" y="52" font-size="12.5" font-weight="600">UTC</text><text class="ink" x="16" y="122" font-size="12.5" font-weight="600">Berlin</text><line class="line" x1="100" y1="48" x2="590" y2="48"/><line class="line" x1="100" y1="118" x2="590" y2="118"/><circle class="dot" cx="120" cy="48" r="4"/><text class="dim" x="120" y="34" font-size="11" text-anchor="middle">23:00</text><line class="curve3" stroke-dasharray="3 3" x1="120" y1="54" x2="120" y2="112"/><circle class="dot" cx="120" cy="118" r="4"/><text class="dim" x="120" y="140" font-size="11" text-anchor="middle">00:00</text><circle class="dot" cx="210" cy="48" r="4"/><text class="dim" x="210" y="34" font-size="11" text-anchor="middle">00:00</text><line class="curve3" stroke-dasharray="3 3" x1="210" y1="54" x2="210" y2="112"/><circle class="dot" cx="210" cy="118" r="4"/><text class="dim" x="210" y="140" font-size="11" text-anchor="middle">01:00</text><circle class="dot" cx="300" cy="48" r="4"/><text class="dim" x="300" y="34" font-size="11" text-anchor="middle">01:00</text><line class="curve3" stroke-dasharray="3 3" x1="300" y1="54" x2="300" y2="112"/><circle class="dot2" cx="300" cy="118" r="4"/><text class="dim" x="300" y="140" font-size="11" text-anchor="middle">03:00</text><circle class="dot" cx="390" cy="48" r="4"/><text class="dim" x="390" y="34" font-size="11" text-anchor="middle">02:00</text><line class="curve3" stroke-dasharray="3 3" x1="390" y1="54" x2="390" y2="112"/><circle class="dot" cx="390" cy="118" r="4"/><text class="dim" x="390" y="140" font-size="11" text-anchor="middle">04:00</text><circle class="dot" cx="480" cy="48" r="4"/><text class="dim" x="480" y="34" font-size="11" text-anchor="middle">03:00</text><line class="curve3" stroke-dasharray="3 3" x1="480" y1="54" x2="480" y2="112"/><circle class="dot" cx="480" cy="118" r="4"/><text class="dim" x="480" y="140" font-size="11" text-anchor="middle">05:00</text><circle class="dot" cx="570" cy="48" r="4"/><text class="dim" x="570" y="34" font-size="11" text-anchor="middle">04:00</text><line class="curve3" stroke-dasharray="3 3" x1="570" y1="54" x2="570" y2="112"/><circle class="dot" cx="570" cy="118" r="4"/><text class="dim" x="570" y="140" font-size="11" text-anchor="middle">06:00</text><text class="ink" x="255.0" y="160" font-size="11" text-anchor="middle">02:00–03:00 missing</text><text class="dim" x="664" y="16" font-size="11" text-anchor="end">30→31 March 2024</text></svg>
  <figcaption>UTC hours move on evenly. Berlin's wall clock jumps from 01:00 to 03:00: one hour that night never happened. In the same zone 12:00 to 12:00 the next day looks like "1 day", but only 23 hours lie between.</figcaption>
</figure>

The rule is simple and standard practice: **store and compute times in UTC;
convert to local time only when showing them to a person.**

In autumn the opposite happens: on the night of 27 October 2024, 02:00–03:00
happened twice in Berlin. A record saying `02:30` matches two different
moments. Python tells them apart with `fold=0` (the first) and `fold=1` (the
second); Section 02 shows the pandas equivalent.

## Unix time

Many systems give time as a single number: **seconds since 1 January 1970
00:00 UTC.** It is very common in APIs, log files and databases.

```python
datetime.fromtimestamp(1710000000, tz=timezone.utc)
# 2024-03-09 16:00:00+00:00

datetime(2024, 3, 9, 16, 0, tzinfo=timezone.utc).timestamp()
# 1710000000.0
```

Two things to watch:

- **Do not forget `tz=timezone.utc`.** Without it Python converts the number
  to the computer's local time, and the same code gives a different result on
  another machine.
- **13-digit numbers are milliseconds.** JavaScript and many APIs use
  milliseconds: `1710000000123` and the like. Divide by 1000 first. Forget
  and Python tries to compute a date 56 thousand years from now and fails.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| `date(9, 3, 2024)` | An error or a wrong date | The order is year, month, day |
| Mixing up `%m` and `%M` | Minutes read instead of the month | `%m` month, `%M` minute |
| Mixing up `%d/%m` and `%m/%d` | A silently wrong date | Check against a row with a day above 12 |
| `timedelta(days=30)` for a month | The wrong day | A calendar offset (Section 04) |
| Week from `isocalendar`, year from `.year` | A week that does not exist | Take both from `isocalendar` |
| Wall-clock durations in a zone with daylight saving | An hour too many or too few | Convert to UTC, then subtract |
| No zone in `fromtimestamp` | A result that depends on the machine | `tz=timezone.utc` |

## Summary

- A date is not text but a **type**: `date`, `datetime`, `time`, and
  `timedelta` for durations. An invalid date cannot be built.
- The order is always **year, month, day**. `weekday()` makes Monday 0,
  `isoweekday()` makes Monday 1.
- Date - date = duration; date + duration = date. `timedelta` knows no months
  or years.
- **`strptime`** reads text, **`strftime`** writes text; `fromisoformat` for
  ISO text. Formats like `03/09/2024` are ambiguous.
- The ISO week can fall into another year at the turn of the year; take the
  year from `isocalendar()` too.
- Time can be naive or aware. **Store and compute in UTC**, convert to local
  time only for display. Across a daylight saving change, "1 day" by the wall
  clock is really 23 hours.
- Unix time is seconds since 1970; convert with `tz=timezone.utc`, divide a
  13-digit number by 1000.
