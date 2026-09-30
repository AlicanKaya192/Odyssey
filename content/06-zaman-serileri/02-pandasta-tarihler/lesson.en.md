# Dates in pandas

In the last section you worked with dates one at a time. In real data a date
is a **column**: thousands of rows, all arriving from a file as text. In this
section we turn that column into real dates, catch the broken rows, and reach
the parts of a date (year, month, day of the week) in one line.

The rules are the same as in Section 01; the only difference is that every
operation now applies to the whole column at once.

## Text or date?

`read_csv` does not turn dates into dates on its own. The first place to look
after reading a file is `dtypes`:

```python
import pandas as pd

sales = pd.read_csv("store_sales.csv")
print(sales.dtypes)
```

```text
date       str
sales    int64
```

The `date` column is **text** (`str`; older pandas versions say `object`).
Date operations do not work on text:

```python
sales["date"].dt.year
# AttributeError: Can only use .dt accessor with datetimelike values
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Text (<code>str</code>)</h4><p>Just a sequence of characters.<br><code>.dt</code> does not work.<br>Comparison is alphabetical.<br>Two dates cannot be subtracted.</p></div>
    <div class="ok"><h4>Date (<code>datetime64</code>)</h4><p>Knows the calendar.<br><code>.dt.year</code>, <code>.dt.day_name()</code>.<br>Comparison is by time.<br>A difference gives a duration.</p></div>
  </div>
  <figcaption>On screen both look like <code>2022-01-01</code>. Only <code>dtypes</code> shows the difference.</figcaption>
</figure>

## `to_datetime`

```python
sales["date"] = pd.to_datetime(sales["date"])
print(sales.dtypes)
```

```text
date     datetime64[us]
sales             int64
```

`datetime64` is pandas' date type; the `us` in brackets is the resolution
(microseconds). The column now knows the calendar:

```python
print(sales["date"].min())                              # 2022-01-01 00:00:00
print(sales["date"].max())                              # 2024-12-31 00:00:00
print((sales["date"].max() - sales["date"].min()).days) # 1095
```

It can also be done in one step while reading the file:

```python
sales = pd.read_csv("store_sales.csv", parse_dates=["date"])
```

**Look at `dtypes` again after converting.** When a conversion fails, pandas
sometimes quietly leaves the column as text; the only way to notice is to
look.

## `Timestamp`: a single moment

Each element of the column is a `Timestamp`. It is pandas' counterpart of
Python's `datetime`; it has the same attributes and adds a few more:

```python
t = pd.Timestamp("2024-03-09 14:37")

print(t.year, t.month, t.day_name())    # 2024 3 Saturday
print(t + pd.Timedelta("2h 15min"))     # 2024-03-09 16:52:00
print(t.normalize())                    # 2024-03-09 00:00:00   zero the time
print(t.floor("h"))                     # 2024-03-09 14:00:00   round down
print(t.round("15min"))                 # 2024-03-09 14:30:00   to the nearest
```

`normalize()`, `floor` and `round` will be very useful later: they are how
records falling on the same day or in the same hour are brought together.

## Day-first dates: a silent error

The ISO format (`2024-03-09`) reads without trouble. Most of the world,
though, writes the day first: `09.03.2024`. With no format given, pandas
**looks at the first row and guesses**, and its guess is month-day-year:

```python
dates = pd.Series(["09.03.2024", "10.03.2024", "11.03.2024"])
print(pd.to_datetime(dates))
```

```text
0   2024-09-03
1   2024-10-03
2   2024-11-03
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>09.03.2024</code></span><span>pandas: <b>3 September</b> · really: 9 March</span></div>
    <div class="anat-row"><span><code>10.03.2024</code></span><span>pandas: <b>3 October</b> · really: 10 March</span></div>
    <div class="anat-row"><span><code>11.03.2024</code></span><span>pandas: <b>3 November</b> · really: 11 March</span></div>
    <div class="anat-row"><span><code>13.03.2024</code></span><span>There is no month 13: only here does an <b>error</b> appear</span></div>
  </div>
  <figcaption>With no format given, the first number is taken for the month. For dates whose day is 12 or less, the mistake stays invisible.</figcaption>
</figure>

**No error, no warning, and the result is wrong.** 9, 10 and 11 March became
3 September, 3 October and 3 November. As long as every day is 12 or less,
pandas cannot notice.

Only when a row with a day above 12 arrives does the guess fail and an error
appear:

```python
pd.to_datetime(pd.Series(["09.03.2024", "13.03.2024"]))
# ValueError: time data "13.03.2024" doesn't match format "%m.%d.%Y"
```

The fix is to **state the format explicitly**, with the codes from Section
01:

```python
pd.to_datetime(dates, format="%d.%m.%Y")
```

```text
0   2024-03-09
1   2024-03-10
2   2024-03-11
```

`dayfirst=True` does the same job, but `format` is better in two ways: it
raises an error on a row that does not fit (you catch bad data early) and it
is faster on large files. **The rule: if the date is not ISO, always write
`format`.**

## Broken dates: `errors="coerce"` and `NaT`

In real files some rows are not even dates. Look at the orders table
(`orders_raw.csv`, 240 rows):

```text
order_id       ordered_at delivered_on  amount
   A1000 03.01.2024 05:12   2024-01-07  225.73
   A1001 04.01.2024 16:13   2024-01-05   63.12
   A1002 05.01.2024 01:24   2024-01-07   35.04
```

```python
orders = pd.read_csv("orders_raw.csv")
pd.to_datetime(orders["ordered_at"], format="%d.%m.%Y %H:%M")
# ValueError: day 31 must be in range 1..29 for month 2 in year 2024
```

A single broken row stops the whole conversion. `errors="coerce"` turns the
broken rows into **`NaT`** (Not a Time; the `NaN` of dates) and carries on:

```python
ordered = pd.to_datetime(orders["ordered_at"],
                         format="%d.%m.%Y %H:%M", errors="coerce")

print(ordered.isna().sum())                        # 3
print(orders.loc[ordered.isna(), "ordered_at"].tolist())
# ['31.02.2024 10:15', 'unknown', '00.00.0000 00:00']
```

The second line matters: **do not use `coerce` blindly.** First look at how
many rows are broken and **which ones**. If 3 rows out of 240 are broken, you
drop them; if 120 turned into `NaT`, the problem is not in the rows but in
the format you wrote.

`NaT` behaves like `NaN`: it equals nothing (not even itself), its
comparisons are `False`, and sums and means skip it. `isna()`, `dropna()` and
`fillna()` work with it too.

## `.dt`: the parts of a date

On a date column, `.dt` reaches a part of every row at once:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>.dt.year</code> <code>.dt.month</code> <code>.dt.day</code></span><span>Year, month, day (numbers)</span></div>
    <div class="anat-row"><span><code>.dt.dayofweek</code></span><span>Day of the week: Monday 0 ... Sunday 6</span></div>
    <div class="anat-row"><span><code>.dt.day_name()</code></span><span>The day's name: <code>Saturday</code></span></div>
    <div class="anat-row"><span><code>.dt.quarter</code></span><span>The quarter: 1–4</span></div>
    <div class="anat-row"><span><code>.dt.hour</code></span><span>The hour: 0–23</span></div>
    <div class="anat-row"><span><code>.dt.normalize()</code></span><span>The date with its time pulled back to midnight</span></div>
  </div>
  <figcaption>Each applies to the whole column and gives one value per row. The full list is in the ".dt Reference" note.</figcaption>
</figure>

```python
sales["weekday"] = sales["date"].dt.day_name()
print(sales.groupby("weekday")["sales"].mean().round(1).sort_values(ascending=False))
```

```text
weekday
Saturday     336.1
Sunday       296.9
Friday       278.9
Thursday     241.1
Wednesday    228.6
Tuesday      220.6
Monday       217.6
```

In Section 00 we did this with a ready-made `weekday` column; now you build
it yourself. The weekend's share is one line too:

```python
weekend = sales["date"].dt.dayofweek >= 5
print(round(sales.loc[weekend, "sales"].sum() / sales["sales"].sum() * 100, 1))   # 34.9
```

Two of the week's seven days carry **34.9%** of sales.

## Filtering by date

A date column can be compared directly with a date written as text; pandas
converts the text itself:

```python
sales[sales["date"] >= "2024-12-01"]                       # 31 rows
sales[sales["date"].between("2024-03-04", "2024-03-10")]   # 7 rows

march = (sales["date"].dt.year == 2024) & (sales["date"].dt.month == 3)
print(sales.loc[march, "sales"].sum())                     # 8919
```

`between` includes both ends. This only works correctly while the column is
**a real date**; on a text column the same line compares alphabetically and,
with day-first dates, returns the wrong rows.

## A duration column

The difference of two date columns is a **duration column**
(`timedelta64`):

```python
delivered = pd.to_datetime(orders["delivered_on"], errors="coerce")
days = (delivered - ordered.dt.normalize()).dt.days

print(days.notna().sum())        # 230
print(round(days.mean(), 2))     # 2.33
print(days.max())                # 8.0
print((days > 3).sum())          # 33
```

Three details:

- `delivered_on` holds only a day, `ordered_at` holds a time as well.
  `normalize()` pulls the order time back to midnight so the difference comes
  out in **whole days**.
- A duration column has `.dt` too: `.dt.days`, `.dt.total_seconds()`.
- If either side is `NaT`, the difference is `NaT`. In 230 of the 240 orders
  both dates are valid; the mean was computed from those alone.

## Time zones

A sensor's records arrived in UTC (the letter `Z` means UTC):

```text
            time_utc  temp_c
2024-03-29T23:00:00Z    16.4
2024-03-30T00:00:00Z    16.9
```

```python
sensor = pd.read_csv("berlin_sensor.csv")
sensor["time_utc"] = pd.to_datetime(sensor["time_utc"])
print(sensor["time_utc"].dtype)            # datetime64[us, UTC]

local = sensor["time_utc"].dt.tz_convert("Europe/Berlin")
print(local.dt.date.value_counts().sort_index())
```

```text
2024-03-30    24
2024-03-31    23
2024-04-01    24
```

**31 March has 23 rows.** The daylight saving change from Section 01, right
there in the table: one hour of that day does not exist. A daily mean is not
affected; a daily **total** adds up one hour too few on that day.

There are two operations, the same distinction as `replace` and
`astimezone` in Section 01:

<figure class="fig">
  <div class="versus">
    <div><h4><code>tz_localize</code>: declare</h4><p>You tell a naive column "these times are in this zone".<br><b>The clock does not change</b>; only a label is added.<br><code>14:30</code> → <code>14:30+03:00</code></p></div>
    <div><h4><code>tz_convert</code>: convert</h4><p>You show an aware column on another zone's clock.<br><b>The clock changes</b>, the moment stays.<br><code>14:30+03:00</code> → <code>11:30+00:00</code></p></div>
  </div>
  <figcaption>On a naive column <code>tz_convert</code> raises an error: it does not know what to convert from. Declare first, then convert.</figcaption>
</figure>

When you declare a zone with daylight saving on a naive column, pandas stops
at the hour that does not exist:

```python
naive = pd.Series(pd.to_datetime(["2024-03-31 01:30", "2024-03-31 02:30"]))
naive.dt.tz_localize("Europe/Berlin")
# ValueError: 2024-03-31 02:30:00 is a nonexistent time due to daylight savings time
```

You say what should happen: `nonexistent="shift_forward"` (move it to 03:00)
or `nonexistent="NaT"`. For the hour that happens twice in autumn the
counterpart is `ambiguous=`. The cleanest way is still the same: **keep the
data in UTC.**

## A Unix time column

For times that arrive as numbers, naming the unit is enough:

```python
pd.to_datetime(events["ts"], unit="s", utc=True)     # seconds
pd.to_datetime(events["ts"], unit="ms", utc=True)    # milliseconds
```

Without `unit`, pandas treats the number as **nanoseconds** and everything
lands in the first seconds of 1970. If all your dates show `1970-01-01`, this
is why.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| Using `.dt` before converting | `AttributeError` | `to_datetime` first, then check `dtypes` |
| Reading day-first dates without a format | Month and day silently swapped | `format="%d.%m.%Y"` |
| Writing `errors="coerce"` and not looking | Half the data may be `NaT` | `isna().sum()` and print the broken rows |
| Comparing a text column with a date | An alphabetical comparison | Convert first |
| Subtracting a date with a time from one without | Fractional, misleading day counts | `normalize()` |
| Mixing up `tz_localize` and `tz_convert` | The moment changes | `localize` to declare, `convert` to convert |
| No `unit` on a Unix column | Every date is in 1970 | `unit="s"` or `"ms"` |

## Summary

- A date from a file is **text.** Convert it with `pd.to_datetime` (or
  `read_csv(parse_dates=...)`), then check `dtypes`.
- If the date is not ISO, **write `format`.** Without it, day-first dates can
  be read wrongly in silence.
- `errors="coerce"` turns broken rows into `NaT`; always look at how many and
  which ones.
- `.dt` gives the parts of a date: `year`, `month`, `dayofweek`,
  `day_name()`, `normalize()`.
- A date column can be filtered with text dates: `>=`, `between`.
- The difference of two date columns is a duration column: `.dt.days`,
  `.dt.total_seconds()`.
- `tz_localize` declares the zone, `tz_convert` converts. A daylight saving
  day has 23 or 25 rows in hourly data.
