# Shifts and Differences

In Section 00 you ran an experiment: to pair today's sales with yesterday's
you sliced the array by hand (`values[:-1]` with `values[1:]`). That pairing
is needed so often in time series work that pandas has tools dedicated to it.

The four tools of this section ask the same question in different forms:
**where does the current value stand against a value from the past?**

- `shift`: bring the past value onto today's row.
- `diff`: how big is the difference?
- `pct_change`: by what percentage did it change?
- `cumsum`: how much has built up from the start until today?

## `shift`: moving the values

```python
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

table = pd.DataFrame({
    "sales": s,
    "lag1": s.shift(1),
    "lag7": s.shift(7),
})
print(table.head(9))
```

```text
            sales   lag1   lag7
date
2022-01-01    305    NaN    NaN
2022-01-02    277  305.0    NaN
2022-01-03    201  277.0    NaN
2022-01-04    182  201.0    NaN
2022-01-05    184  182.0    NaN
2022-01-06    211  184.0    NaN
2022-01-07    251  211.0    NaN
2022-01-08    299  251.0  305.0
2022-01-09    278  299.0  277.0
```

`shift(1)` pushes every value **one row down**: the row of 2 January now
holds the sales of 1 January. So on every row "today" and "yesterday" sit
side by side. `shift(7)` does the same for a week.

Two details:

- **The rows at the start are empty.** The first day has no yesterday; for
  `lag7` the first seven days have no last week. As many `NaN` values appear
  as the size of the shift.
- **The dates stay put, the values move.** The index is the same.

A value brought from the past is called a **lag**. The experiment from
Section 00 is now one line:

```python
print(round(s.corr(s.shift(1)), 3))    # 0.695
print(round(s.corr(s.shift(7)), 3))    # 0.958
```

<figure class="fig">
  <svg viewBox="0 0 680 230" width="680" xmlns="http://www.w3.org/2000/svg"><line class="line" x1="44" y1="182.4" x2="666" y2="182.4"/><text class="dim" x="38" y="185.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="145.7" x2="666" y2="145.7"/><text class="dim" x="38" y="149.2" font-size="10.5" text-anchor="end">0.25</text><line class="grid" x1="44" y1="109.1" x2="666" y2="109.1"/><text class="dim" x="38" y="112.6" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="44" y1="72.4" x2="666" y2="72.4"/><text class="dim" x="38" y="75.9" font-size="10.5" text-anchor="end">0.75</text><line class="grid" x1="44" y1="35.7" x2="666" y2="35.7"/><text class="dim" x="38" y="39.2" font-size="10.5" text-anchor="end">1</text><line class="line" x1="44" y1="200" x2="666" y2="200"/><line class="line" x1="67.0" y1="200" x2="67.0" y2="204"/><text class="dim" x="67.0" y="216" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="239.8" y1="200" x2="239.8" y2="204"/><text class="dim" x="239.8" y="216" font-size="10.5" text-anchor="middle">7</text><line class="line" x1="441.4" y1="200" x2="441.4" y2="204"/><text class="dim" x="441.4" y="216" font-size="10.5" text-anchor="middle">14</text><line class="line" x1="643.0" y1="200" x2="643.0" y2="204"/><text class="dim" x="643.0" y="216" font-size="10.5" text-anchor="middle">21</text><rect class="dot3" x="58.1" y="80.5" width="17.9" height="101.9" rx="3" opacity="0.55"/><rect class="dot3" x="86.9" y="141.8" width="17.9" height="40.6" rx="3" opacity="0.55"/><rect class="dot3" x="115.7" y="166.8" width="17.9" height="15.6" rx="3" opacity="0.55"/><rect class="dot3" x="144.5" y="167.6" width="17.9" height="14.8" rx="3" opacity="0.55"/><rect class="dot3" x="173.3" y="143.0" width="17.8" height="39.4" rx="3" opacity="0.55"/><rect class="dot3" x="202.1" y="82.1" width="17.8" height="100.3" rx="3" opacity="0.55"/><rect class="dot3" x="230.9" y="42.0" width="17.8" height="140.4" rx="3" opacity="0.55"/><rect class="dot3" x="259.7" y="82.2" width="17.8" height="100.2" rx="3" opacity="0.55"/><rect class="dot3" x="288.5" y="143.7" width="17.8" height="38.7" rx="3" opacity="0.55"/><rect class="dot3" x="317.3" y="169.8" width="17.8" height="12.6" rx="3" opacity="0.55"/><rect class="dot3" x="346.1" y="170.4" width="17.8" height="12.0" rx="3" opacity="0.55"/><rect class="dot3" x="374.9" y="145.3" width="17.8" height="37.1" rx="3" opacity="0.55"/><rect class="dot3" x="403.7" y="83.7" width="17.8" height="98.7" rx="3" opacity="0.55"/><rect class="dot3" x="432.5" y="43.1" width="17.8" height="139.3" rx="3" opacity="0.55"/><rect class="dot3" x="461.3" y="83.9" width="17.8" height="98.5" rx="3" opacity="0.55"/><rect class="dot3" x="490.1" y="146.0" width="17.8" height="36.4" rx="3" opacity="0.55"/><rect class="dot3" x="518.9" y="172.0" width="17.8" height="10.4" rx="3" opacity="0.55"/><rect class="dot3" x="547.6" y="172.6" width="17.9" height="9.8" rx="3" opacity="0.55"/><rect class="dot3" x="576.4" y="147.7" width="17.9" height="34.7" rx="3" opacity="0.55"/><rect class="dot3" x="605.2" y="85.5" width="17.9" height="96.9" rx="3" opacity="0.55"/><rect class="dot3" x="634.0" y="44.4" width="17.9" height="138.0" rx="3" opacity="0.55"/><rect class="dot" x="230.9" y="42.0" width="17.8" height="140.4" rx="3" opacity="0.9"/><rect class="dot" x="432.5" y="43.1" width="17.8" height="139.3" rx="3" opacity="0.9"/><rect class="dot" x="634.0" y="44.4" width="17.9" height="138.0" rx="3" opacity="0.9"/><text class="ink" x="239.8" y="34.6" font-size="11" text-anchor="middle">0.96</text><text class="ink" x="441.4" y="35.8" font-size="11" text-anchor="middle">0.95</text><text class="ink" x="643.0" y="37.1" font-size="11" text-anchor="middle">0.94</text><text class="dim" x="67.0" y="73.2" font-size="10.5" text-anchor="middle">0.69</text><text class="dim" x="124.6" y="159.5" font-size="10.5" text-anchor="middle">0.11</text></svg>
  <figcaption>The correlation between today's sales and sales k days earlier (horizontal axis: k). A peak every 7 days: the shop remembers a week ago very well, three days ago hardly at all.</figcaption>
</figure>

The chart shows the shop's memory. Sales 3 days ago have almost nothing to do
with today (0.106); those 7 and 14 days ago are very strongly linked. This
chart is called **autocorrelation**, and the whole of Section 12 is devoted
to it.

## Past and future

`shift` takes negative numbers too:

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4><code>shift(1)</code>: a lag</h4><p>Brings <b>the past</b> onto today's row.<br>A value that really was known that day.<br>Safe as a feature.</p></div>
    <div class="no"><h4><code>shift(-1)</code>: a lead</h4><p>Brings <b>the future</b> onto today's row.<br>A value not yet known that day.<br>Only for the target (answer) column.</p></div>
  </div>
  <figcaption>The test question: on the day you forecast, could you have known this value? If not, it cannot be a feature.</figcaption>
</figure>

```python
s.shift(-1)     # tomorrow's value on today's row
```

It looks innocent, but it is the most common source of leakage in time
series. The **inputs** of a forecasting model must always look at the past
(`shift(1)`, `shift(7)`). `shift(-1)` is used only to build the **target**:
when you say "forecast tomorrow from today's data", tomorrow is the answer
column, not a feature.

## `diff`: the difference

The difference between today and yesterday is `s - s.shift(1)`. For short:

```python
change = s.diff()

print(change.head(4).tolist())           # [nan, -28.0, -76.0, -19.0]
print(round(change.abs().mean(), 1))     # 36.8
print(change.idxmax().date(), change.max())   # 2023-12-30 106.0
print(change.idxmin().date(), change.min())   # 2024-01-01 -139.0
```

Sales move by 36.8 units on average from one day to the next. The biggest
drop is 1 January 2024: the day after New Year's Eve.

`diff(7)` compares today with **the same day last week**:

```python
print(s.diff(7).loc["2024-03-09"])       # 12.0     384 - 372

print(round(s.diff().std(), 1))          # 46.1
print(round(s.diff(7).std(), 1))         # 17.1
```

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="202.2" x2="666" y2="202.2"/><text class="dim" x="38" y="205.7" font-size="10.5" text-anchor="end">−100</text><line class="grid" x1="44" y1="157.8" x2="666" y2="157.8"/><text class="dim" x="38" y="161.3" font-size="10.5" text-anchor="end">−50</text><line class="line" x1="44" y1="113.4" x2="666" y2="113.4"/><text class="dim" x="38" y="116.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="44" y1="69.1" x2="666" y2="69.1"/><text class="dim" x="38" y="72.6" font-size="10.5" text-anchor="end">50</text><line class="grid" x1="44" y1="24.7" x2="666" y2="24.7"/><text class="dim" x="38" y="28.2" font-size="10.5" text-anchor="end">100</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">1 Mar</text><line class="line" x1="365.4" y1="220" x2="365.4" y2="224"/><text class="dim" x="365.4" y="236" font-size="10.5" text-anchor="middle">1 Apr</text><line class="line" x1="666.0" y1="220" x2="666.0" y2="224"/><text class="dim" x="666.0" y="236" font-size="10.5" text-anchor="middle">30 Apr</text><polyline class="curve3" style="stroke-width:1.4" points="44.0,67.3 54.4,51.3 64.7,160.5 75.1,171.2 85.5,106.3 95.8,136.5 106.2,107.2 116.6,73.5 126.9,28.2 137.3,178.3 147.7,182.7 158.0,93.0 168.4,112.6 178.8,99.2 189.1,88.6 199.5,34.4 209.9,179.2 220.2,198.7 230.6,95.7 241.0,79.7 251.3,114.3 261.7,98.4 272.1,69.1 282.4,135.6 292.8,186.3 303.2,108.1 313.5,113.4 323.9,110.8 334.3,76.2 344.6,46.9 355.0,142.8 365.4,192.5 375.7,121.4 386.1,106.3 396.5,88.6 406.8,81.5 417.2,63.7 427.6,178.3 437.9,180.0 448.3,88.6 458.7,102.8 469.0,108.1 479.4,85.0 489.8,59.3 500.1,147.2 510.5,205.8 520.9,101.9 531.2,93.9 541.6,110.8 552.0,79.7 562.3,57.5 572.7,147.2 583.1,196.0 593.4,114.3 603.8,93.0 614.2,122.3 624.5,66.4 634.9,70.8 645.3,125.9 655.6,173.8 666.0,144.5"/><polyline class="curve" style="stroke-width:2.4" points="44.0,134.8 54.4,117.9 64.7,125.9 75.1,89.5 85.5,95.7 95.8,131.2 106.2,119.7 116.6,125.9 126.9,102.8 137.3,120.6 147.7,132.1 158.0,118.8 168.4,94.8 178.8,86.8 189.1,101.9 199.5,108.1 209.9,109.0 220.2,125.0 230.6,127.7 241.0,94.8 251.3,109.9 261.7,119.7 272.1,154.3 282.4,110.8 292.8,98.4 303.2,110.8 313.5,144.5 323.9,141.0 334.3,118.8 344.6,96.6 355.0,103.7 365.4,109.9 375.7,123.2 386.1,116.1 396.5,93.9 406.8,99.2 417.2,116.1 427.6,151.6 437.9,139.2 448.3,106.3 458.7,102.8 469.0,122.3 479.4,125.9 489.8,121.4 500.1,90.4 510.5,116.1 520.9,129.4 531.2,120.6 541.6,123.2 552.0,117.9 562.3,116.1 572.7,116.1 583.1,106.3 593.4,118.8 603.8,117.9 614.2,129.4 624.5,116.1 634.9,129.4 645.3,108.1 655.6,85.9 666.0,116.1"/><line class="curve3" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">diff()  vs yesterday</text><line class="curve" x1="240" y1="22" x2="258" y2="22"/><text class="ink" x="264" y="26" font-size="11">diff(7)  vs last week</text></svg>
  <figcaption>March–April 2024. The grey line is the difference against the day before: it draws the same zigzag every week. The purple line is the difference against the same day last week: the weekly pattern is gone, leaving a narrow band around zero.</figcaption>
</figure>

The spread of the daily differences is 46.1; that of the weekly differences
17.1. The reason is plain: comparing Saturday with Friday measures the
week's pattern, comparing Saturday with last Saturday measures **the real
change.** A difference taken by going back one full season is called a
**seasonal difference**, and it removes the seasonality from the series.
Section 11 uses it for stationarity.

Differencing can be undone: `diff` and `cumsum` are each other's inverse.

```python
back = s.diff().cumsum() + s.iloc[0]      # gives the series back, bar the first value
```

## `pct_change`: percentage change

A difference is an absolute number; its size depends on the level of the
series. A percentage change does not:

```python
print(round(s.pct_change().loc["2024-03-09"] * 100, 1))     # 33.3   vs yesterday
print(round(s.pct_change(7).loc["2024-03-09"] * 100, 1))    # 3.2    vs last week
```

On Saturday 9 March sales rose 33.3% on the day before. That is not news; it
happens every Saturday. Against the previous Saturday the rise is 3.2%: that
is the real information.

**What you compare with decides what you are saying.** At the monthly level:

```python
daily_mean = s.resample("ME").mean()

mom = daily_mean.pct_change() * 100       # against the previous month
yoy = daily_mean.pct_change(12) * 100     # against the same month last year

print(mom.round(1).loc["2024-01":"2024-04"].tolist())   # [-11.5, -0.3, -1.7, -7.3]
print(yoy.round(1).loc["2024-01":"2024-04"].tolist())   # [11.9, 12.8, 16.4, 10.5]
```

The same four months, two different stories. Against the previous month sales
**fall every month**; against last year they **grow by more than 10% every
month.** Both are true:

- A **month-on-month** change contains the seasonality. After the December
  peak, January falls every year.
- A **year-on-year** change compares the same season, so it leaves
  seasonality out and shows the trend.

In a seasonal series, the answer to "are we growing?" is in the year-on-year
change.

## The "same day last year" trap

For a year-on-year comparison in daily data, how many days do you go back?
365 is the first thing that comes to mind:

```python
print(s.loc["2024-03-09"])                # 384   a Saturday
print(s.shift(365).loc["2024-03-09"])     # 265   10 March 2023, a Friday
print(s.shift(364).loc["2024-03-09"])     # 323   11 March 2023, a Saturday
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>9 March 2024</span><span>a Saturday · sales <b>384</b></span></div>
    <div class="anat-row"><span>365 days earlier</span><span>10 March 2023, a <b>Friday</b> · 265 · growth looks like <b>45%</b></span></div>
    <div class="anat-row"><span>364 days earlier</span><span>11 March 2023, a <b>Saturday</b> · 323 · growth of <b>19%</b></span></div>
  </div>
  <figcaption>365 = 52 × 7 + 1. A slip of one day means comparing a Saturday with a Friday. 364 is exactly 52 weeks.</figcaption>
</figure>

Going back 365 days lands on **a different day of the week**, because 365 is
not a multiple of 7. Compare a Saturday with a Friday and growth looks like
45%; compare a Saturday with a Saturday and it is 19%.

364 days is exactly 52 weeks. Measure the difference over the whole year:

```python
yoy_364 = (s / s.shift(364) - 1) * 100
yoy_365 = (s / s.shift(365) - 1) * 100

print(round(yoy_364.loc["2024"].std(), 1))    # 7.2
print(round(yoy_365.loc["2024"].std(), 1))    # 18.7
```

The comparison with 365 swings by 18.7 points from day to day; most of that
is not growth but days of the week getting mixed up. **In a daily series with
a weekly pattern, use 364 days for a yearly comparison.**

## `shift` goes wrong on missing days

`shift(1)` does not mean "one day earlier"; it means **"one row earlier".**
When the rows are complete and in order the two are the same thing. When they
are not:

```python
messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

print(fixed.loc["2024-07-13":"2024-07-19"])
```

```text
date
2024-07-13    344
2024-07-14    312
2024-07-18    253
2024-07-19    292
```

```python
print(fixed.diff().loc["2024-07-18"])                  # -59.0
print(fixed.asfreq("D").diff().loc["2024-07-18"])      # nan
```

The first line says "-59 against yesterday" for 18 July. But the previous row
is 14 July: **four days earlier.** There is no error; the number looks
reasonable and is wrong.

Once the series is put on the calendar (`asfreq("D")`) there is an empty row
for 17 July, and the difference honestly comes out as `NaN`. This was the
reason for the rule in Section 03: **a series must be regular before you
compute differences and lags.**

## `cumsum`: accumulation

Let us go the other way: from changes to a total.

```python
ytd = s.loc["2024"].cumsum()

print(ytd.iloc[-1])                          # 107611   the year-end total
print((ytd >= 50000).idxmax().date())        # 2024-06-28
```

`cumsum` writes on every row the total up to that day: **year to date.** In
2024 the 50 thousand mark was reached on 28 June; in 2023 the same threshold
was reached on 24 July. Plotting two years cumulatively shows how the gap
opens up over the year.

## Returns

In price series, a percentage change has a special name: a **return**.

```python
close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
r = close.pct_change()

print(round(r.std() * 100, 2))                      # 1.72   daily volatility
print(r.idxmax().date(), round(r.max() * 100, 2))   # 2023-03-02 5.3
```

**Percentages do not add up.** Add up the daily returns to get the total
return of the three years and you get the wrong number:

```python
print(round((close.iloc[-1] / close.iloc[0] - 1) * 100, 1))   # 66.1   the truth
print(round(r.sum() * 100, 1))                                # 62.3   wrong
print(round(((1 + r).cumprod().iloc[-1] - 1) * 100, 1))       # 66.1   right
```

Returns build up by **multiplying**: a price that rises 10% and then falls
10% does not come back to where it started, it ends at 99
(`100 × 1.10 × 0.90`). That is why a cumulative return is not `cumsum` but
`(1 + r).cumprod()`.

If you want a return that can be added, use the **logarithmic return**:

```python
import numpy as np

log_r = np.log(close).diff()
print(round((np.exp(log_r.sum()) - 1) * 100, 1))     # 66.1
```

The details are in the "Returns and Accumulation" note.

One last observation that will matter a great deal later:

```python
print(round(close.corr(close.shift(1)), 4))     # 0.9927
print(round(r.corr(r.shift(1)), 3))             # 0.045
```

Today's **price** is tied almost one to one to yesterday's price. Today's
**return** is independent of yesterday's return. The level of the price looks
predictable but its change is not. This kind of series is called a random
walk, and we come back to it in Sections 11–12.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| Using `shift(-1)` as a feature | The model sees the future | A positive `shift` for features |
| `shift` / `diff` on a series with missing days | "Yesterday" is really days ago | `asfreq` first |
| `shift(365)` for a yearly comparison | A different day of the week | `shift(364)` |
| Looking at month-on-month change in a seasonal series | Seasonality is taken for a "fall" | Year-on-year change |
| Adding up daily returns | The wrong total return | `(1 + r).cumprod()` or log returns |
| Forgetting the `NaN` values at the start | The model fails or rows slip | `dropna()`; know how many rows go |
| Mixing up percent and percentage points | 10% to 12% "rose by 2 percent" | 2 **points**, 20 percent |

## Summary

- **`shift(k)`** brings the value from k rows earlier onto today's row: a
  lag. The first k rows are `NaN`.
- **`shift(-k)`** brings the future; only for building the target.
- **`diff(k)`** is the difference against k rows earlier. `diff(7)` is a
  seasonal difference: it removes the weekly pattern.
- **`pct_change(k)`** is the percentage change. Month on month shows the
  seasonality, year on year the trend.
- For a yearly comparison in daily data use **364 days**; 365 shifts the day
  of the week.
- `shift` and `diff` count **rows**, not days. Call `asfreq` first.
- **`cumsum`** gives the running total. Returns build up by multiplying:
  `(1 + r).cumprod()`.
