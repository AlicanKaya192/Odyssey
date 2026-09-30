# Periods and Calendars

So far every timestamp was a **point**: `2024-03-09`, or `2024-03-09 14:30`.
But "March 2024" is not a point; it is a **span** of 31 days. So are "the
first quarter", "week 10" and "the year 2024".

The calendar is also uneven: months run from 28 to 31 days, there are
weekends, there are holidays. Questions such as "one month later", "three
business days later" or "the last day of the month" cannot be answered with a
fixed duration.

This section covers those two faces of the calendar: **spans** and
**calendar arithmetic.**

## A moment and a span

<figure class="fig">
  <div class="versus">
    <div><h4><code>Timestamp</code>: a moment</h4><p>A single <b>point</b> on the calendar.<br><code>2024-03-09</code><br>"When did it happen?"</p></div>
    <div class="ok"><h4><code>Period</code>: a span</h4><p>A <b>stretch</b> with a start and an end.<br><code>2024-03</code> = 1 March 00:00 → 31 March 23:59<br>"In which period did it happen?"</p></div>
  </div>
  <figcaption>Daily sales build up within a day, monthly sales within a month. A span is the better language for totals, a point for events.</figcaption>
</figure>

```python
import pandas as pd

p = pd.Period("2024-03", freq="M")

print(p)                 # 2024-03
print(p.start_time)      # 2024-03-01 00:00:00
print(p.end_time)        # 2024-03-31 23:59:59.999999
print(p.days_in_month)   # 31
print(p + 1)             # 2024-04
```

A `Period` holds a span with its start and end; `+ 1` moves to the next span.
`to_period` tells you which span a day falls into:

```python
day = pd.Timestamp("2024-03-09")

print(day.to_period("M"))   # 2024-03
print(day.to_period("Q"))   # 2024Q1
print(day.to_period("Y"))   # 2024
print(day.to_period("W"))   # 2024-03-04/2024-03-10
```

**Careful: `"M"` for periods, `"ME"` for `date_range`.** In the last section
writing `"M"` gave an error; here it is the other way round:

```python
pd.Period("2024-03", freq="ME")
# ValueError: Invalid frequency: ME ... for Period, please use 'M'
```

The logic: `"ME"` is a **point** (the last day of the month), `"M"` is a
**span** (the whole month). A period works with spans, so it wants `M`, `Q`,
`Y`.

## Monthly totals

The most direct way to add a daily series up into months is to assign each
day to its month and group:

```python
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

monthly = s.groupby(s.index.to_period("M")).sum()

print(len(monthly))                  # 36
print(monthly.loc["2024-01":"2024-04"])
```

```text
date
2024-01    9103
2024-02    8491
2024-03    8919
2024-04    8003
Freq: M, Name: sales, dtype: int64
```

The index is now a `PeriodIndex`: each row is not a day but a month.
Selecting by date works the same way (`monthly.loc["2024-03"]` → 8919). The
highest month is `monthly.idxmax()` → `2024-12`, 11335.

Section 05 does the same job with `resample`, which is more flexible.
`to_period` is the clearest way to say **which period a date belongs to**,
and it is always handy for grouping and labelling.

## Months are not equally long

Look at the table again: February's total (8491) is below March's (8919).
Did sales go badly in February?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>January 2024</span><span>total <b>9103</b> · 31 days · <b>293.6</b> a day</span></div>
    <div class="anat-row"><span>February 2024</span><span>total <b>8491</b> · 29 days · <b>292.8</b> a day</span></div>
    <div class="anat-row"><span>March 2024</span><span>total <b>8919</b> · 31 days · <b>287.7</b> a day</span></div>
    <div class="anat-row"><span>April 2024</span><span>total <b>8003</b> · 30 days · <b>266.8</b> a day</span></div>
  </div>
  <figcaption>By total, February is behind March. By daily mean, it is ahead. The difference comes not from sales but from the calendar.</figcaption>
</figure>

**No.** February has 29 days, March 31. Look at the daily mean and the order
flips: February **292.8**, March **287.7**. February's total is lower because
it is two days shorter; the shop sold more per day that month.

```python
daily_mean = s.groupby(s.index.to_period("M")).mean().round(1)
days = monthly.index.days_in_month
```

This is one of the most common misreadings of a time series. **Before
comparing monthly totals, divide by the number of days.** Month length alone
makes a difference of up to 10% (28 versus 31 days); the real change is often
smaller than that.

## Quarters and weeks

```python
quarterly = s.groupby(s.index.to_period("Q")).sum()
print(quarterly.loc["2024"])
```

```text
2024Q1    26513
2024Q2    24146
2024Q3    26025
2024Q4    30927
```

A weekly period starts on Monday and ends on Sunday, and its label shows both
ends: `2024-03-04/2024-03-10`. The boundaries are the same as the ISO week
from Section 01, but without the year-end confusion: the label simply writes
the dates.

Some companies' fiscal year does not start in January. For a fiscal year
ending in March use `to_period("Q-MAR")`: 9 March 2024 is `2024Q4`, 9 April
2024 is `2025Q1`.

## From a period back to a date

To draw a chart or combine with another date-indexed series you may need to
turn the period back into a point:

```python
monthly.to_timestamp()             # month starts: 2022-01-01, 2022-02-01, ...
monthly.to_timestamp(how="end")    # month ends
```

Which day stands for a month is a choice: the start or the end? Know which
one you picked and do not mix them; when you join two monthly series, one at
month start and the other at month end, **no rows match.**

## Moving by the calendar: `DateOffset`

In Section 01 you saw that `timedelta` knows no months. Its pandas
counterpart that does is `DateOffset`:

<figure class="fig">
  <div class="versus">
    <div><h4><code>Timedelta</code>: a duration</h4><p>A fixed length: days, hours, minutes.<br><code>31 Jan + 30 days</code> → <b>1 March</b><br>For measuring durations.</p></div>
    <div class="ok"><h4><code>DateOffset</code>: the calendar</h4><p>Knows months and years.<br><code>31 Jan + 1 month</code> → <b>29 Feb</b><br>For moving along the calendar.</p></div>
  </div>
  <figcaption>"One month later" can be 28, 29, 30 or 31 days. The calendar knows which; a duration does not.</figcaption>
</figure>

```python
t = pd.Timestamp("2024-01-31")

print(t + pd.Timedelta(days=30))        # 2024-03-01   30 days later
print(t + pd.DateOffset(months=1))      # 2024-02-29   one month later
```

February has no 31st, so `DateOffset` lands on the **last valid day** of the
month. The same rule shows up elsewhere:

```python
pd.Timestamp("2024-03-31") + pd.DateOffset(months=1)    # 2024-04-30
pd.Timestamp("2024-02-29") + pd.DateOffset(years=1)     # 2025-02-28
pd.Timestamp("2024-03-09") - pd.DateOffset(years=1)     # 2023-03-09   a year earlier
```

The last line will be used a lot: comparing with "the same day last year" is
the simplest way to take yearly seasonality out of the picture.

## Month end, month start

There are ready-made offsets for **moving** a date to a particular point on
the calendar:

```python
from pandas.tseries.offsets import MonthEnd, MonthBegin

d = pd.Timestamp("2024-03-09")

print(d + MonthEnd(0))      # 2024-03-31   the end of this month
print(d + MonthEnd(1))      # 2024-03-31   the next month end (still this month)
print(d - MonthBegin(1))    # 2024-03-01   the start of this month
print(d + MonthBegin(1))    # 2024-04-01   the start of next month
```

`MonthEnd(0)` means "if you are already at a month end stay there, otherwise
go to the month end". `MonthEnd(1)` jumps to the following month end when you
are already on one (`2024-03-31 + MonthEnd(1)` → `2024-04-30`). The
difference only shows when the date falls exactly on a month end, which is
precisely why it slips through.

Applied to a whole index it gives a feature such as "days left until month
end":

```python
days_left = ((s.index + MonthEnd(0)) - s.index).days     # 30, 29, 28, ...
```

In businesses with a payday, a billing day or a month-end close, sales move
with this number.

## Business days

Many series exist only on business days: the stock market, bank
transactions, office traffic. `BDay` (business day) skips weekends:

```python
from pandas.tseries.offsets import BDay

friday = pd.Timestamp("2024-03-08")

print(friday + BDay(1))                 # 2024-03-11   Monday
print(friday + BDay(3))                 # 2024-03-13   Wednesday
print(len(pd.bdate_range("2024-03-01", "2024-03-31")))    # 21
print(len(pd.bdate_range("2024-01-01", "2024-12-31")))    # 262
```

The number of business days is not the same in every month either:

<figure class="fig">
  <svg viewBox="0 0 680 220" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="190.0" x2="666" y2="190.0"/><text class="dim" x="38" y="193.5" font-size="10.5" text-anchor="end">18</text><line class="grid" x1="44" y1="162.7" x2="666" y2="162.7"/><text class="dim" x="38" y="166.2" font-size="10.5" text-anchor="end">19</text><line class="grid" x1="44" y1="135.3" x2="666" y2="135.3"/><text class="dim" x="38" y="138.8" font-size="10.5" text-anchor="end">20</text><line class="grid" x1="44" y1="108.0" x2="666" y2="108.0"/><text class="dim" x="38" y="111.5" font-size="10.5" text-anchor="end">21</text><line class="grid" x1="44" y1="80.7" x2="666" y2="80.7"/><text class="dim" x="38" y="84.2" font-size="10.5" text-anchor="end">22</text><line class="grid" x1="44" y1="53.3" x2="666" y2="53.3"/><text class="dim" x="38" y="56.8" font-size="10.5" text-anchor="end">23</text><line class="grid" x1="44" y1="26.0" x2="666" y2="26.0"/><text class="dim" x="38" y="29.5" font-size="10.5" text-anchor="end">24</text><line class="line" x1="44" y1="190" x2="666" y2="190"/><line class="line" x1="74.6" y1="190" x2="74.6" y2="194"/><text class="dim" x="74.6" y="206" font-size="10.5" text-anchor="middle">Jan</text><line class="line" x1="125.6" y1="190" x2="125.6" y2="194"/><text class="dim" x="125.6" y="206" font-size="10.5" text-anchor="middle">Feb</text><line class="line" x1="176.6" y1="190" x2="176.6" y2="194"/><text class="dim" x="176.6" y="206" font-size="10.5" text-anchor="middle">Mar</text><line class="line" x1="227.5" y1="190" x2="227.5" y2="194"/><text class="dim" x="227.5" y="206" font-size="10.5" text-anchor="middle">Apr</text><line class="line" x1="278.5" y1="190" x2="278.5" y2="194"/><text class="dim" x="278.5" y="206" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="329.5" y1="190" x2="329.5" y2="194"/><text class="dim" x="329.5" y="206" font-size="10.5" text-anchor="middle">Jun</text><line class="line" x1="380.5" y1="190" x2="380.5" y2="194"/><text class="dim" x="380.5" y="206" font-size="10.5" text-anchor="middle">Jul</text><line class="line" x1="431.5" y1="190" x2="431.5" y2="194"/><text class="dim" x="431.5" y="206" font-size="10.5" text-anchor="middle">Aug</text><line class="line" x1="482.5" y1="190" x2="482.5" y2="194"/><text class="dim" x="482.5" y="206" font-size="10.5" text-anchor="middle">Sep</text><line class="line" x1="533.4" y1="190" x2="533.4" y2="194"/><text class="dim" x="533.4" y="206" font-size="10.5" text-anchor="middle">Oct</text><line class="line" x1="584.4" y1="190" x2="584.4" y2="194"/><text class="dim" x="584.4" y="206" font-size="10.5" text-anchor="middle">Nov</text><line class="line" x1="635.4" y1="190" x2="635.4" y2="194"/><text class="dim" x="635.4" y="206" font-size="10.5" text-anchor="middle">Dec</text><rect class="dot" x="58.8" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="109.8" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="160.8" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="211.7" y="80.7" width="31.6" height="109.3" rx="3" opacity="0.9"/><rect class="dot" x="262.7" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="313.7" y="135.3" width="31.6" height="54.7" rx="3" opacity="0.9"/><rect class="dot" x="364.7" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="415.7" y="80.7" width="31.6" height="109.3" rx="3" opacity="0.9"/><rect class="dot" x="466.7" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="517.6" y="53.3" width="31.6" height="136.7" rx="3" opacity="0.9"/><rect class="dot" x="568.6" y="108.0" width="31.6" height="82.0" rx="3" opacity="0.9"/><rect class="dot" x="619.6" y="80.7" width="31.6" height="109.3" rx="3" opacity="0.9"/><text class="ink" x="74.6" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="125.6" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="176.6" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="227.5" y="73.8" font-size="11" text-anchor="middle">22</text><text class="ink" x="278.5" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="329.5" y="128.5" font-size="11" text-anchor="middle">20</text><text class="ink" x="380.5" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="431.5" y="73.8" font-size="11" text-anchor="middle">22</text><text class="ink" x="482.5" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="533.4" y="46.5" font-size="11" text-anchor="middle">23</text><text class="ink" x="584.4" y="101.2" font-size="11" text-anchor="middle">21</text><text class="ink" x="635.4" y="73.8" font-size="11" text-anchor="middle">22</text></svg>
  <figcaption>Business days per month in 2024 (Monday–Friday, before holidays). The fewest is 20 in June, the most 23. The vertical axis starts at 18.</figcaption>
</figure>

June has 20 business days, January 23: **a 15% difference.** The monthly total
of anything that happens only on business days (invoices issued, units
produced) swings this much even when nothing changes.

The stock price series (`stock_price.csv`) is an example: 782 rows, all on
weekdays.

```python
close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

print(pd.infer_freq(close.index))           # B
print(close.asfreq("D").isna().sum())       # 312
```

Put this series on the daily calendar with `asfreq("D")` and 312 "missing"
days appear. None of them is missing: the market was closed. **Use the
series' own frequency** (`"B"`); treating weekends as missing data and
filling them would invent prices that never existed.

## Holidays

`BDay` only knows weekends. It knows nothing of public holidays, because they
differ from country to country. You supply the list:

```python
from pandas.tseries.offsets import CustomBusinessDay

holidays = pd.read_csv("holidays_2024.csv", parse_dates=["date"])["date"]
workday = CustomBusinessDay(holidays=holidays)

print(len(pd.date_range("2024-01-01", "2024-12-31", freq=workday)))    # 250
print(len(pd.date_range("2024-04-01", "2024-04-30", freq=workday)))    # 18
```

12 of the 262 business days fall on holidays: **250 working days.** (Two of
the 14 holidays land on a Sunday anyway.) April drops from 22 business days
to 18: the Ramadan Feast takes three days and 23 April one.

The difference becomes concrete in calculations such as a delivery date. An
order placed on Tuesday 9 April was promised in "3 business days":

```python
order = pd.Timestamp("2024-04-09")

print(order + BDay(3))        # 2024-04-12   the third day of the holiday!
print(order + 3 * workday)    # 2024-04-17
```

Without a holiday calendar the promised day is a day nobody works.

Using a holiday as a **feature** is one line too:

```python
is_holiday = s.index.isin(holidays)
```

For countries whose weekend is Friday–Saturday:
`CustomBusinessDay(weekmask="Sun Mon Tue Wed Thu")`.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| `Period(..., freq="ME")` | `Invalid frequency` | `M`, `Q`, `Y` for periods |
| Comparing monthly totals directly | The short month looks "bad" | Divide by the number of days (or business days) |
| `Timedelta(days=30)` for "one month later" | The wrong day | `pd.DateOffset(months=1)` |
| Mixing up `MonthEnd(1)` and `MonthEnd(0)` | A month-end date moves a month ahead | `MonthEnd(0)` for "the end of this month" |
| `asfreq("D")` on a business-day series | Weekends look "missing" | `asfreq("B")` |
| Promising a date with plain `BDay` | It lands on a holiday | `CustomBusinessDay(holidays=...)` |
| Mixing month-start and month-end labels | Rows do not match when joining | Pick one and use it everywhere |

## Summary

- A `Timestamp` is a **moment**, a `Period` is a **span**. `to_period("M")`
  tells you which month a day falls into.
- Period aliases are `M`, `Q`, `Y`, `W`; the `ME` of `date_range` does not
  work here.
- `s.groupby(s.index.to_period("M")).sum()` is a monthly total;
  `to_timestamp()` turns a period back into a date.
- **Months are not equal.** Divide by the number of days or business days
  before comparing.
- `DateOffset` moves by the calendar (months, years); `MonthEnd` and
  `MonthBegin` move a date to a point on the calendar.
- `BDay` skips weekends; for holidays use `CustomBusinessDay` with your own
  list. The frequency of a business-day series is `B`.
