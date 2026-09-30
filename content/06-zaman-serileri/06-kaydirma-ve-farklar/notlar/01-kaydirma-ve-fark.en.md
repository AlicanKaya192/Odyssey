## Four tools

| Tool | Equivalent | Gives |
|---|---|---|
| `s.shift(k)` | — | The value k rows earlier |
| `s.diff(k)` | `s - s.shift(k)` | The absolute difference |
| `s.pct_change(k)` | `s / s.shift(k) - 1` | The relative change (0.05 = 5%) |
| `s.cumsum()` | — | The total from the start until today |
| `s.cumprod()` | — | The product from the start until today |
| `s.cummax()`, `s.cummin()` | — | The highest / lowest so far |

Without `k` it is 1. All of them count **rows**, not calendar days.

## Which `k`?

| Data | Yesterday | Same day last week | Last year |
|---|---|---|---|
| Hourly | `24` | `168` | `8736` (52 weeks) |
| Daily | `1` | `7` | `364` |
| Business days | `1` | `5` | about `252` |
| Weekly | — | `1` | `52` |
| Monthly | — | — | `12` |
| Quarterly | — | — | `4` |

## The names of a change

| Name | Short | What it shows |
|---|---|---|
| Day on day | DoD | Mostly the weekly pattern |
| Week on week | WoW | Short-term change; the weekly pattern is out |
| Month on month | MoM | Contains seasonality; affected by month length |
| Quarter on quarter | QoQ | Contains seasonality |
| Year on year | YoY | Seasonality is out; shows the trend |
| Year to date | YTD | Accumulation; `cumsum` |

## Percent and percentage points

If a rate goes from 10% to 12%:

- it rose by **2 percentage points** (12 - 10);
- it rose by **20 percent** (12 / 10 - 1).

Saying "it rose by 2 percent" is wrong. On rate series (conversion rate,
interest, share) `diff` gives points and `pct_change` gives percent; write
down which one you are reporting.

## The base effect

A year-on-year change depends on two things: this year and **last year.** If
the same period last year was unusually low (a lockdown, a stock problem),
this year's growth looks exaggerated; if it was unusually high, this year
looks like a "fall". This is called the base effect.

Near a base of zero a percentage change loses its meaning: going from 2 to 6
is "200% growth". With small numbers, write the absolute difference too.

## Building a table of lags

```python
lags = pd.DataFrame({"y": s})
for k in (1, 7, 14, 364):
    lags[f"lag{k}"] = s.shift(k)

lags = lags.dropna()          # as many rows go as the largest lag
```

If the largest lag is 364, the first 364 rows are dropped. With three years
of data you lose a year; take that into account when choosing lags.

## Building the target

"Forecast h steps ahead from what is known today":

```python
h = 7
data = pd.DataFrame({
    "lag0": s,                 # today
    "lag7": s.shift(7),        # last week
    "target": s.shift(-h),     # 7 days ahead: THE ANSWER
}).dropna()
```

`shift(-h)` appears only in the `target` column. None of the feature columns
may have a negative shift.

## Shifting by time when days are missing

```python
s.shift(1)               # one ROW down: the values move, the index stays
s.shift(freq="D")        # one DAY ahead: the index moves, the values stay
s - s.shift(freq="D")    # aligned by date: days with no yesterday are NaN
```

`shift(freq=...)` does not count rows; it moves time. In a series with
missing days, use this for a real "difference against yesterday", or call
`asfreq("D")` first.

## What differencing changes

| Operation | Removes |
|---|---|
| `s.diff()` | The level and a linear trend |
| `s.diff(7)` | The weekly seasonality (and the trend) |
| `s.diff(7).diff()` | Both |
| `np.log(s).diff()` | Close to a percentage change; also evens out growing volatility |

Every difference **amplifies the noise** and takes rows from the start.
Difference as much as needed and no more (Section 11).
