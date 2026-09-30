## The pattern

```python
s.resample("<frequency>").<operation>()
```

First the bins (`"W"`, `"ME"`, `"h"`, `"15min"`...), then the operation that
reduces what is in a bin to one number.

## Operations

| Operation | Gives | On an empty bin |
|---|---|---|
| `sum()` | The total | `0` |
| `sum(min_count=1)` | The total | `NaN` |
| `mean()` | The mean | `NaN` |
| `median()` | The median | `NaN` |
| `max()`, `min()` | The largest, the smallest | `NaN` |
| `first()`, `last()` | The bin's first / last valid value | `NaN` |
| `count()` | The number of valid values | `0` |
| `size()` | The number of rows (`NaN` included) | `0` |
| `std()` | The standard deviation | `NaN` |
| `ohlc()` | Open, high, low, close | `NaN` |
| `nunique()` | The number of distinct values | `0` |
| `agg(["sum", "mean"])` | Several summaries, one per column | — |
| `agg(function)` | Your own function | — |

On a table (DataFrame), a separate operation per column:

```python
df.resample("W").agg({"sales": "sum", "price": "mean", "stock": "last"})
```

## Which value, which operation

| Kind of value | Example | Downsampling | Upsampling |
|---|---|---|---|
| A flow (it accumulates) | Sales, consumption, visits, rainfall | `sum` | Spread it (divide) |
| A level at a moment | Price, stock, balance | `last` | `ffill` |
| A measurement at a moment | Temperature, speed, load | `mean` (`max` for the peak) | `interpolate` |
| A rate | Conversion rate, occupancy | A weighted mean | `ffill` |
| A count | Events, errors, number of orders | `sum` or `count` | Spread it |

**Averaging rates is a trap.** The plain mean of daily conversion rates does
not give the weekly rate; add up numerator and denominator separately, then
divide:

```python
weekly = df.resample("W").agg({"orders": "sum", "visits": "sum"})
weekly["rate"] = weekly["orders"] / weekly["visits"]
```

## The label and the closed end

| Frequency | Bin | Label |
|---|---|---|
| `"D"`, `"h"`, `"15min"` | Start included, end excluded | The **start** of the bin |
| `"W"` (= `"W-SUN"`) | Monday–Sunday | The **end** of the bin (Sunday) |
| `"W-MON"` | Tuesday–Monday | Monday |
| `"ME"`, `"QE"`, `"YE"` | Calendar month / quarter / year | The period's **last** day |
| `"MS"`, `"QS"`, `"YS"` | The same bins | The period's **first** day |

```python
# start the week on Sunday, label it by its start
s.resample("W", label="left", closed="left").sum()

# for "end of hour" readings
s.resample("h", label="right", closed="right").mean()

# start the day at 06:00
load.resample("24h", offset="6h").sum()
```

If a meter writes its value at the **end** of the hour (the 14:00 row
describes 13:00–14:00), the default binning is an hour off; then use
`closed="right", label="right"`.

## Checking the bins

```python
counts = s.resample("W").count()
weekly = s.resample("W").sum()
full = weekly[counts == 7]                 # full weeks only

s.resample("W").sum(min_count=7)           # make an incomplete bin NaN
s.resample("ME").agg(["sum", "count"])     # see the two side by side
```

The expected number of observations: 7 days in a week, 24 hours in a day,
`index.days_in_month` in a month.

## `resample`, `asfreq`, `groupby`

| Tool | What it does | When |
|---|---|---|
| `s.resample("ME").sum()` | Bins and summarises | To change the frequency |
| `s.asfreq("D")` | Opens rows, computes nothing | To make gaps visible |
| `s.groupby(s.index.to_period("M")).sum()` | Groups by period and summarises | When you want a period index |
| `s.groupby(s.index.month).mean()` | Pools the same month of **every year** | A seasonal profile (Section 09) |

The last row is often confused: `resample("ME")` gives 36 months (each month
of each year separately), `groupby(index.month)` gives 12 rows (all the
Januaries together).
