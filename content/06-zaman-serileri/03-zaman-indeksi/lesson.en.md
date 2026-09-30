# The Time Index

In the last section the date was a **column**. In this section we move it into
the table's **index**. It looks like a small change, but every time series
tool in pandas relies on it: selecting by date, taking a whole month with one
word, finding missing days, and the resampling, shifting and rolling windows
of the sections ahead.

Once the date is in the index, pandas sees the table as a time series.

## Moving the date into the index

```python
import pandas as pd

sales = pd.read_csv("store_sales.csv", parse_dates=["date"])
sales = sales.set_index("date")
s = sales["sales"]

print(type(s.index).__name__)   # DatetimeIndex
print(s.head(3))
```

```text
date
2022-01-01    305
2022-01-02    277
2022-01-03    201
Name: sales, dtype: int64
```

It can be done in one step while reading:

```python
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
```

`s` is now a single-column series: the date on the left, the value on the
right. For the rest of the track we will mostly keep a time series in this
shape.

## Selecting by date

Instead of a row number **you write a date**:

```python
print(s.loc["2024-03-09"])        # 384         one day
print(len(s.loc["2024-03"]))      # 31          all of March
print(s.loc["2024-03"].sum())     # 8919
print(len(s.loc["2024"]))         # 366         the whole year
print(round(s.loc["2024"].mean(), 1))   # 294.0
```

Writing `"2024-03"` is enough; pandas reads it as "all of March 2024". In the
last section you found the same total with two conditions on `dt.year` and
`dt.month`; here it is one word.

## Slicing

```python
week = s.loc["2024-03-04":"2024-03-10"]
print(len(week), week.sum())                        # 7 1978

print(len(s.loc["2024-01":"2024-03"]))              # 91   the first quarter
print(len(s.loc[:"2022-01-07"]))                    # 7    from the start to that day
print(len(s.loc["2024-12-25":]))                    # 7    from that day to the end
```

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4><code>loc</code>: by label</h4><p><code>s.loc["2024-03-04":"2024-03-10"]</code><br>You write dates.<br><b>Both ends included</b>: 7 days.</p></div>
    <div><h4><code>iloc</code>: by position</h4><p><code>s.iloc[0:7]</code><br>You write row numbers.<br><b>End excluded</b>: 7 rows, 0 to 6.</p></div>
  </div>
  <figcaption>With time series you mostly use <code>loc</code>: saying "the first week of March" is both easier and safer than "row 796 to row 803".</figcaption>
</figure>

**A date slice includes both ends.** `"2024-03-04":"2024-03-10"` gives seven
days; `iloc[0:7]` gives seven rows from 0 to 6 and leaves out row 7. When you
work with dates you do not have to wonder whether the last day is included:
it is.

A single day that does not exist is an error; a range that does not exist is
an empty result:

```python
s.loc["2025-01-01"]                       # KeyError
len(s.loc["2025-01-01":"2025-02-01"])     # 0
```

## The parts of the index itself

On a column you wrote `.dt`; on the index it is not needed:

```python
print(s.index.min(), s.index.max())     # 2022-01-01 ... 2024-12-31
print(s.index[-1] - s.index[0])         # 1095 days

weekend = s[s.index.dayofweek >= 5]
print(round(weekend.mean(), 1))         # 316.5

print(s.groupby(s.index.month).mean().round(1).loc[12])   # 327.3
```

`s.index.year`, `s.index.month`, `s.index.dayofweek`, `s.index.day_name()`...
The whole `.dt` list from the last section works directly on the index.

## Real files are messy

The file so far was clean. The same shop's 2024 records arrived from another
system like this (`sales_messy.csv`, 362 rows):

```text
      date  sales
2024-04-13    351
2024-11-28    297
2024-07-22    232
2024-01-25    281
```

There are three separate problems: **the order is scrambled, some days are
written twice, and some days are missing altogether.** None of them shows
when you look at the table; we catch each with its own question.

<figure class="fig">
  <div class="flow">
    <span class="node">Date into the index</span><span class="arrow">→</span>
    <span class="node">Sort<br><code>sort_index()</code></span><span class="arrow">→</span>
    <span class="node">Resolve repeats<br><code>groupby(level=0)</code></span><span class="arrow">→</span>
    <span class="node">Find the gaps<br><code>date_range</code></span><span class="arrow">→</span>
    <span class="node acc">Onto the calendar<br><code>asfreq</code></span>
  </div>
  <figcaption>The first five things to do with a new time series, in this order. The order matters: it cannot go onto the calendar while dates repeat, and cannot be sliced while unsorted.</figcaption>
</figure>

### 1. Order

```python
messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]

print(messy.index.is_monotonic_increasing)     # False
messy.loc["2024-03-04":"2024-03-10"]
# KeyError: Value based partial slicing on non-monotonic DatetimeIndexes ...
```

A date range **cannot be selected** from an index that is not in order. The
fix is one line:

```python
messy = messy.sort_index()
```

**Always call `sort_index()` after moving the date into the index.** It does
no harm and changes nothing on data that is already in order.

### 2. Repeated dates

```python
print(messy.index.is_unique)                   # False
print(messy.index.duplicated().sum())          # 4
print(messy.loc["2024-03-05"].tolist())        # [157, 105]
```

There are **two rows** for 5 March. Asking for one day and getting two values
breaks every calculation that follows. What to do depends on what the data
means:

| Case | Fix |
|---|---|
| The day's sales were written in two parts | Add them: `groupby(level=0).sum()` |
| The same record arrived twice | Drop one: `~index.duplicated()` |
| A corrected value arrived later | Take the last: `groupby(level=0).last()` |
| Two measurements of the same moment | Average: `groupby(level=0).mean()` |

Here the records are parts: 157 + 105 = 262, the real value in the clean
file.

```python
fixed = messy.groupby(level=0).sum()
print(len(fixed), fixed.index.is_unique)       # 358 True
```

`level=0` means "group by the index". **pandas cannot know which one to
choose; you have to ask the system that produced the data.** The wrong choice
(dropping a part instead of adding them) halves that day's sales.

### 3. Missing dates

There are 358 rows; 2024 has 366 days. Which days are not there?

```python
full = pd.date_range(fixed.index.min(), fixed.index.max(), freq="D")
missing = full.difference(fixed.index)

print(len(full), len(missing))                 # 366 8
print(missing.strftime("%Y-%m-%d").tolist())
```

```text
['2024-02-10', '2024-02-11', '2024-04-23', '2024-07-15', '2024-07-16',
 '2024-07-17', '2024-10-29', '2024-12-25']
```

`date_range` produces the full calendar that should be there; `difference`
gives the days we do not have.

Why do missing days matter so much? Because time series tools assume that
**"the previous row is yesterday"**. If the row after 14 July is 18 July, "the
change since yesterday" is really the change over four days, and no error
appears.

## Frequency and `asfreq`

A regular series has a **frequency**: daily, hourly, monthly. pandas can
infer it from the index:

```python
print(pd.infer_freq(s.index))        # D      the clean series: daily
print(pd.infer_freq(fixed.index))    # None   it cannot tell, because of the gaps
```

`asfreq("D")` puts the series on the full daily calendar; it opens a row for
each missing day and leaves its value **empty** (`NaN`):

```python
regular = fixed.asfreq("D")

print(len(regular), regular.isna().sum())           # 366 8
print(regular.loc["2024-07-14":"2024-07-18"].tolist())
# [312.0, nan, nan, nan, 253.0]
```

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="324.9" y="14" width="60.2" height="186" opacity="0.8" style="stroke:none"/><line class="grid" x1="44" y1="185.0" x2="666" y2="185.0"/><text class="dim" x="38" y="188.5" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="134.4" x2="666" y2="134.4"/><text class="dim" x="38" y="137.9" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="83.7" x2="666" y2="83.7"/><text class="dim" x="38" y="87.2" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="33.0" x2="666" y2="33.0"/><text class="dim" x="38" y="36.5" font-size="10.5" text-anchor="end">350</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="54.0" y1="200" x2="54.0" y2="204"/><text class="dim" x="54.0" y="216" font-size="10.5" text-anchor="middle">1 Jul</text><line class="line" x1="194.5" y1="200" x2="194.5" y2="204"/><text class="dim" x="194.5" y="216" font-size="10.5" text-anchor="middle">8 Jul</text><line class="line" x1="334.9" y1="200" x2="334.9" y2="204"/><text class="dim" x="334.9" y="216" font-size="10.5" text-anchor="middle">15 Jul</text><line class="line" x1="475.4" y1="200" x2="475.4" y2="204"/><text class="dim" x="475.4" y="216" font-size="10.5" text-anchor="middle">22 Jul</text><line class="line" x1="615.8" y1="200" x2="615.8" y2="204"/><text class="dim" x="615.8" y="216" font-size="10.5" text-anchor="middle">29 Jul</text><polyline class="curve" points="54.0,182.0 74.1,170.9 94.2,162.7 114.2,131.3 134.3,81.7 154.4,37.1 174.4,75.6 194.5,169.8 214.5,168.8 234.6,157.7 254.7,119.2 274.7,100.9 294.8,39.1 314.9,71.5"/><polyline class="curve" points="395.1,131.3 415.2,91.8 435.3,40.1 455.3,79.6 475.4,152.6 495.5,152.6 515.5,152.6 535.6,132.3 555.6,66.5 575.7,32.0 595.8,80.6 615.8,152.6 635.9,133.4 656.0,145.5"/><circle class="dot" cx="54.0" cy="182.0" r="3.2"/><circle class="dot" cx="74.1" cy="170.9" r="3.2"/><circle class="dot" cx="94.2" cy="162.7" r="3.2"/><circle class="dot" cx="114.2" cy="131.3" r="3.2"/><circle class="dot" cx="134.3" cy="81.7" r="3.2"/><circle class="dot" cx="154.4" cy="37.1" r="3.2"/><circle class="dot" cx="174.4" cy="75.6" r="3.2"/><circle class="dot" cx="194.5" cy="169.8" r="3.2"/><circle class="dot" cx="214.5" cy="168.8" r="3.2"/><circle class="dot" cx="234.6" cy="157.7" r="3.2"/><circle class="dot" cx="254.7" cy="119.2" r="3.2"/><circle class="dot" cx="274.7" cy="100.9" r="3.2"/><circle class="dot" cx="294.8" cy="39.1" r="3.2"/><circle class="dot" cx="314.9" cy="71.5" r="3.2"/><circle class="dot" cx="395.1" cy="131.3" r="3.2"/><circle class="dot" cx="415.2" cy="91.8" r="3.2"/><circle class="dot" cx="435.3" cy="40.1" r="3.2"/><circle class="dot" cx="455.3" cy="79.6" r="3.2"/><circle class="dot" cx="475.4" cy="152.6" r="3.2"/><circle class="dot" cx="495.5" cy="152.6" r="3.2"/><circle class="dot" cx="515.5" cy="152.6" r="3.2"/><circle class="dot" cx="535.6" cy="132.3" r="3.2"/><circle class="dot" cx="555.6" cy="66.5" r="3.2"/><circle class="dot" cx="575.7" cy="32.0" r="3.2"/><circle class="dot" cx="595.8" cy="80.6" r="3.2"/><circle class="dot" cx="615.8" cy="152.6" r="3.2"/><circle class="dot" cx="635.9" cy="133.4" r="3.2"/><circle class="dot" cx="656.0" cy="145.5" r="3.2"/><text class="ink" x="355.0" y="18.5" font-size="11" text-anchor="middle">15–17 July: no records</text></svg>
  <figcaption>July 2024 after <code>asfreq("D")</code>. There are rows for the three days but no values; the line breaks there. The gap is now visible both in the table and on the chart.</figcaption>
</figure>

The gap is now **visible**: there is a row for every day and the empty ones
stand out. Two notes:

- The column turned into floats (`312.0`), because `NaN` cannot live in an
  integer column.
- We do **not fill the gaps now.** What to fill them with (the previous
  value, an interpolated value, zero) is a separate decision and the subject
  of Section 13. Only if you can say "no record means no sales" use
  `asfreq("D", fill_value=0)`.

`asfreq` does not work while dates are repeated
(`cannot reindex on an axis with duplicate labels`); that is why the order
matters: **sort, resolve the repeats, then put it on the calendar.**

## `date_range`: producing a calendar

We just produced the full calendar with `date_range`. You give two of three
things: start, end, count.

```python
pd.date_range("2024-03-01", periods=3, freq="D")      # 1, 2, 3 March
pd.date_range("2024-01-01", "2024-06-30", freq="ME")  # month ends: 31 Jan ... 30 Jun
pd.date_range("2024-01-01", periods=3, freq="MS")     # month starts: 1 Jan, 1 Feb, 1 Mar
pd.date_range("2024-03-09 08:00", periods=4, freq="6h")   # 08:00, 14:00, 20:00, 02:00
pd.date_range("2024-03-04", "2024-03-17", freq="B")   # business days: 10 days
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>D</code></span><span>Day</span></div>
    <div class="anat-row"><span><code>h</code> · <code>min</code> · <code>s</code></span><span>Hour, minute, second (lower case)</span></div>
    <div class="anat-row"><span><code>B</code></span><span>Business day: Monday–Friday</span></div>
    <div class="anat-row"><span><code>W</code> · <code>W-MON</code></span><span>Week (ending Sunday) · week ending Monday</span></div>
    <div class="anat-row"><span><code>ME</code> · <code>MS</code></span><span>Month end · month start</span></div>
    <div class="anat-row"><span><code>QE</code> · <code>YE</code></span><span>Quarter end · year end</span></div>
  </div>
  <figcaption>A number can go in front: <code>15min</code>, <code>6h</code>, <code>2W</code>. The full list is in the "Frequency Aliases" note.</figcaption>
</figure>

**Older sources show `freq="M"` and `"H"`; they no longer work.** In current
pandas a month end is `"ME"` and an hour is lower-case `"h"`. Write `"M"` and
you get `Invalid frequency: M`.

## Selecting by time of day in hourly data

When the index also holds a time, selection goes one level deeper by the same
logic. Hourly electricity load (`energy_hourly.csv`):

```python
load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)["load_mw"]

print(len(load.loc["2024-03-15"]))                              # 24   that whole day
print(len(load.loc["2024-03-15 08:00":"2024-03-15 12:00"]))     # 5    a range of hours
```

To select **by time of day** regardless of the date there are two helpers:

```python
day = load.between_time("08:00", "18:00")
night = load.between_time("22:00", "06:00")

print(round(day.mean(), 1), round(night.mean(), 1))   # 1038.1 768.4
print(len(load.at_time("18:00")))                     # 61   18:00 of every day
```

`between_time` understands a range that crosses midnight (`22:00`–`06:00`).
Daytime load is 1.35 times the night's: a seasonality tied to the hour of the
day.

## Alignment: pandas matches by date

When you add two series, pandas looks not at the row order but at **the
index**:

```python
a = s.loc["2024-01"]                        # 31 days
b = s.loc["2024-01-15":"2024-02-15"]        # 32 days

total = a + b
print(len(total), total.notna().sum(), total.isna().sum())   # 46 17 29
```

The result is as long as the union of the two ranges (46 days). On the 17
days present in both there is a sum; on the 29 days present in only one there
is `NaN`. **The same dates were matched, and the ones without a partner stayed
empty.** This is safe behaviour: had you added the two by position, 1 January
and 15 January would have been added together in silence.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| `loc["2024-03"]` without the date in the index | `KeyError` | `set_index("date")` |
| Not calling `sort_index()` | `KeyError` when slicing | Sort right after setting the index |
| Assuming "end excluded" as with `iloc` | One day too many | A date slice takes both ends |
| Dropping repeats at random | The day's value is incomplete | Add / take the last, by what the data means |
| Not looking for missing days | "The previous row" is not yesterday | `date_range` + `difference`, then `asfreq` |
| `freq="M"`, `"H"` | `Invalid frequency` | `"ME"`, `"h"` |
| `fillna(0)` right after `asfreq` | Missing days count as "no sales" | Decide what the gap means first |

## Summary

- Put the date in the **index** (`set_index`, or `index_col=...,
  parse_dates=True`) and call **`sort_index()`** right away.
- Select by date: `loc["2024-03-09"]`, `loc["2024-03"]`, `loc["2024"]`. A
  slice includes **both ends**.
- The parts of the index need no `.dt`: `s.index.month`, `s.index.dayofweek`.
- Three checks: `is_monotonic_increasing` (is it in order), `is_unique` (are
  there repeats), `date_range(...).difference(index)` (is anything missing).
- Resolve repeats by what the data means (`groupby(level=0)`), then put the
  series on the full calendar with **`asfreq`** so the gaps show as `NaN`.
- `date_range` produces a calendar. Aliases: `D`, `h`, `min`, `B`, `W`, `ME`,
  `MS`, `QE`, `YE`.
- In hourly data, `between_time` and `at_time`. When two series are added,
  pandas aligns them by date.
