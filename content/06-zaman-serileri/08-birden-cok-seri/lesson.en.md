# Many Series at Once

So far we have always worked with a single series: one shop, one sensor, one
stock. In real work a series almost never comes alone. Four shops, fifty
products, two hundred sensors: the same measure, for different units, in the
same table.

The question of this section: how do you apply everything you have learned
(lags, differences, resampling, windows) **to each series separately**, and
how do you combine series with each other?

## Two shapes

The 2024 sales of four shops (`stores.csv`, 1291 rows):

```text
      date store  sales
2024-01-01     A    291
2024-01-01     B    180
2024-01-01     C    256
2024-01-02     A    288
2024-01-02     B    190
2024-01-02     C    248
```

This is the **long** shape: each row is a (date, shop) pair. The same data
can also be kept in a **wide** shape: each shop a column, each date a row.

<figure class="fig">
  <div class="versus">
    <div><h4>Long shape</h4><p>One <b>(date, shop)</b> per row.</p><pre><code class="language-text">date        store  sales
2024-05-01      A    269
2024-05-01      B    174
2024-05-01      C    226
2024-05-01      D    106</code></pre></div>
    <div><h4>Wide shape</h4><p>One <b>date</b> per row, one column per shop.</p><pre><code class="language-text">date          A    B    C    D
2024-05-01  269  174  226  106
2024-05-02  ...</code></pre></div>
  </div>
  <figcaption>The same four numbers, laid out two ways. When a new shop arrives the long shape adds rows; the wide shape adds a column.</figcaption>
</figure>

```python
import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

print(wide.shape)               # (366, 4)
print(wide.head(3))
```

```text
store           A      B      C   D
date
2024-01-01  291.0  180.0  256.0 NaN
2024-01-02  288.0  190.0  248.0 NaN
2024-01-03  287.0  191.0  269.0 NaN
```

The way back is `melt`:

```python
back = wide.reset_index().melt(id_vars="date", var_name="store", value_name="sales")
```

Both carry the same information; which one is convenient depends on the job.
Files and databases mostly come in the long shape; the wide shape is easier
for comparing, correlating and plotting.

## The wide shape shows what is missing

The long table had 1291 rows; the wide table has 366 × 4 = 1464 cells. The
difference is the (date, shop) pairs that **had no row at all** in the long
table:

```python
print(long.groupby("store").size().to_dict())
# {'A': 366, 'B': 366, 'C': 314, 'D': 245}

print(wide.isna().sum().to_dict())
# {'A': 0, 'B': 0, 'C': 52, 'D': 121}

print(wide["D"].first_valid_index().date())     # 2024-05-01
```

In the long shape a missing row **did not show**; in the wide shape it
surfaced as `NaN`. It is the same effect as `asfreq` in Section 03: putting
the table on a regular grid makes the gaps visible.

## Each series separately: `groupby`

This is where the biggest trap of the long shape lies. Write `shift(1)` out
of habit to bring yesterday's sales:

```python
long["lag_wrong"] = long["sales"].shift(1)
print(long.head(5))
```

```text
        date store  sales  lag_wrong
0 2024-01-01     A    291        NaN
1 2024-01-01     B    180      291.0
2 2024-01-01     C    256      180.0
3 2024-01-02     A    288      256.0
4 2024-01-02     B    190      288.0
```

As shop B's "yesterday" you got shop A's sales **of the same day.** `shift`
moves rows; the rows alternate between shops, so the previous row is a
different shop.

The right way is to shift **within each shop**:

```python
long["lag1"] = long.groupby("store")["sales"].shift(1)
print(long[long["date"] == "2024-01-02"])
```

```text
        date store  sales  lag1
3 2024-01-02     A    288  291.0
4 2024-01-02     B    190  180.0
5 2024-01-02     C    248  256.0
```

Let us measure the difference:

```python
print(round(long["sales"].corr(long["sales"].shift(1)), 3))   # -0.33
print(round(long["sales"].corr(long["lag1"]), 3))             # 0.866
```

With the wrong lag the correlation comes out **negative**; with the right one
it is 0.866. **There is no error**; the wrong column slips silently into a
model and ruins it.

The rule: **in the long shape, `shift`, `diff`, `pct_change`, `rolling` and
`cumsum` always go with `groupby`.** For window operations use `transform`:

```python
long["ma7"] = long.groupby("store")["sales"].transform(lambda x: x.rolling(7).mean())
```

The wide shape does not have this trap: each column is already one series,
and operations apply column by column (`wide.shift(1)`,
`wide.rolling(7).mean()`).

## Resampling each series

For weekly totals per shop in the long shape, `groupby` is used together with
`Grouper`:

```python
weekly = long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()
print(weekly.loc["A"].head(2))
```

```text
date
2024-01-07    2296
2024-01-14    2297
```

`pd.Grouper(key="date", freq="W")` means "cut the date column into weekly
bins". The result has a two-level index: shop and week. In the wide shape the
same job is one line: `wide.resample("W").sum()`.

## Comparing series

The shops are at very different levels:

```python
print(long.groupby("store")["sales"].agg(["sum", "mean", "count"]).round(1))
```

```text
          sum   mean  count
store
A      116462  318.2    366
B       65806  179.8    366
C       78034  248.5    314
D       41877  170.9    245
```

Raw numbers cannot answer "which one is growing faster?": A is the
top-selling shop every single day. Start them all from the same point and the
picture changes. Index the monthly means, taking May, the first month all
four shops are open, as 100:

```python
monthly = wide.resample("ME").mean()
index = monthly / monthly.loc["2024-05-31"] * 100

print(index.loc["2024-12-31"].round(1).to_dict())
# {'A': 120.3, 'B': 116.8, 'C': 114.1, 'D': 182.2}
```

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="195.6" x2="666" y2="195.6"/><text class="dim" x="38" y="199.1" font-size="10.5" text-anchor="end">100</text><line class="grid" x1="44" y1="154.9" x2="666" y2="154.9"/><text class="dim" x="38" y="158.4" font-size="10.5" text-anchor="end">120</text><line class="grid" x1="44" y1="114.2" x2="666" y2="114.2"/><text class="dim" x="38" y="117.7" font-size="10.5" text-anchor="end">140</text><line class="grid" x1="44" y1="73.5" x2="666" y2="73.5"/><text class="dim" x="38" y="77.0" font-size="10.5" text-anchor="end">160</text><line class="grid" x1="44" y1="32.8" x2="666" y2="32.8"/><text class="dim" x="38" y="36.3" font-size="10.5" text-anchor="end">180</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">May</text><line class="line" x1="132.9" y1="220" x2="132.9" y2="224"/><text class="dim" x="132.9" y="236" font-size="10.5" text-anchor="middle">Jun</text><line class="line" x1="221.7" y1="220" x2="221.7" y2="224"/><text class="dim" x="221.7" y="236" font-size="10.5" text-anchor="middle">Jul</text><line class="line" x1="310.6" y1="220" x2="310.6" y2="224"/><text class="dim" x="310.6" y="236" font-size="10.5" text-anchor="middle">Aug</text><line class="line" x1="399.4" y1="220" x2="399.4" y2="224"/><text class="dim" x="399.4" y="236" font-size="10.5" text-anchor="middle">Sep</text><line class="line" x1="488.3" y1="220" x2="488.3" y2="224"/><text class="dim" x="488.3" y="236" font-size="10.5" text-anchor="middle">Oct</text><line class="line" x1="577.1" y1="220" x2="577.1" y2="224"/><text class="dim" x="577.1" y="236" font-size="10.5" text-anchor="middle">Nov</text><line class="line" x1="666.0" y1="220" x2="666.0" y2="224"/><text class="dim" x="666.0" y="236" font-size="10.5" text-anchor="middle">Dec</text><polyline class="curve" style="stroke-width:2.4" points="44.0,195.6 132.9,194.6 221.7,198.7 310.6,186.1 399.4,178.2 488.3,169.5 577.1,159.9 666.0,154.2"/><polyline class="curve2" style="stroke-width:2.4" points="44.0,195.6 132.9,194.0 221.7,191.7 310.6,185.4 399.4,177.3 488.3,168.3 577.1,161.4 666.0,161.3"/><polyline class="curve3" style="stroke-width:2.4" points="44.0,195.6 132.9,195.2 221.7,197.4 310.6,184.7 399.4,185.3 488.3,176.2 577.1,171.0 666.0,167.0"/><polyline class="curve4" style="stroke-width:2.4" points="44.0,195.6 132.9,179.4 221.7,165.9 310.6,131.2 399.4,107.5 488.3,77.2 577.1,50.1 666.0,28.2"/><line class="curve3" stroke-dasharray="4 4" x1="44" y1="195.6" x2="666" y2="195.6"/><line class="curve" x1="54" y1="22" x2="72" y2="22"/><text class="ink" x="78" y="26" font-size="11">A</text><line class="curve2" x1="107" y1="22" x2="125" y2="22"/><text class="ink" x="131" y="26" font-size="11">B</text><line class="curve3" x1="160" y1="22" x2="178" y2="22"/><text class="ink" x="184" y="26" font-size="11">C</text><line class="curve4" x1="213" y1="22" x2="231" y2="22"/><text class="ink" x="237" y="26" font-size="11">D</text></svg>
  <figcaption>Monthly mean sales, May = 100. D, the smallest in raw numbers, is the fastest growing on the index: 182 in December. The other three shops are between 114 and 120; the differences between them are small next to the year-end seasonality.</figcaption>
</figure>

The smallest shop is the fastest growing: D grew 82% from May to December.
Its share of the total changes accordingly:

```python
quarterly = wide.resample("QE").sum()
share = quarterly.div(quarterly.sum(axis=1), axis=0) * 100
print(share.round(1))
```

```text
store          A     B     C     D
date
2024-03-31  43.8  25.5  30.7   0.0
2024-06-30  39.6  22.3  26.7  11.4
2024-09-30  36.3  20.5  24.2  18.9
2024-12-31  35.7  19.7  22.9  21.7
```

A's share went from 43.8 to 35.7. A did not shrink; the pie grew.

## Do they move together?

```python
print(wide.corr().round(2).loc["A"].to_dict())
# {'A': 1.0, 'B': 0.46, 'C': 0.88, 'D': 0.8}

print(wide.resample("W").mean().corr().round(2).loc["A"].to_dict())
# {'A': 1.0, 'B': 0.83, 'C': 0.77, 'D': 0.94}
```

In daily data the correlation between A and B is 0.46; on weekly means it is
0.83. A daily correlation largely measures **the weekly pattern**: A has a
strong weekend, B a weak one. Go down to weekly and that pattern is gone,
leaving the shared trend and the shared yearly pattern. Whether two series
are "related" depends on the frequency you look at.

## Two kinds of missing

Not every `NaN` in the wide table means the same thing:

<figure class="fig">
  <div class="versus">
    <div><h4>Closed: shop C, Sundays</h4><p>The shop exists; that day there are <b>no</b> sales.<br>Counting it as <b>zero</b> in a total is right.<br>For a mean there are two options: per open day or per calendar day.</p></div>
    <div class="no"><h4>Absent: shop D, before May</h4><p>The shop has <b>not opened</b> yet.<br>Counting zero is <b>wrong</b>: it turns months that did not exist into "bad months".<br>The right thing is to leave that stretch out.</p></div>
  </div>
  <figcaption>In the table both are <code>NaN</code>. The data does not say which is which; someone who knows the data does.</figcaption>
</figure>

**Shop C is closed on Sundays.** There is no record that day because there
are no sales. Counting it as zero in a total is right:

```python
print(round(wide["C"].mean(), 1))              # 248.5   mean of the days it is open
print(round(wide["C"].fillna(0).mean(), 1))    # 213.2   per calendar day
```

The two numbers answer two different questions: "how much does it sell on a
day it is open?" and "how much revenue does it bring per day on average?".
Both are legitimate; you need to know which one you are computing.

**Shop D opened on 1 May.** The `NaN` before that is not "zero sales" but "no
shop":

```python
print(round(wide["D"].mean(), 1))              # 170.9
print(round(wide["D"].fillna(0).mean(), 1))    # 114.4   wrong
```

Filling with zero lowers D's mean by a third and makes four months that did
not exist look like "four very bad months".

The same distinction applies to a total:

```python
total = wide.sum(axis=1)
print(total.loc["2024-04-30"], total.loc["2024-05-01"])    # 626.0 775.0
```

`sum` skips `NaN` values. Overnight the total jumped from 626 to 775; sales
did not rise, **a fourth shop entered the total.** In a combined series such
a jump is a structural break; when you analyse it you either compare the same
set of shops (A + B + C) or flag the break.

## Finding the value in effect: `merge_asof`

Shop A's unit price changes a few times a year. The price list holds only
**the days it changed** (`prices.csv`):

```text
valid_from  price
2024-01-01   19.9
2024-03-15   21.5
2024-06-01   22.9
2024-09-10   21.9
2024-11-20   24.5
```

We want to multiply each day's sales by the price **in effect** that day. An
ordinary join (`merge`) matches only rows whose dates are exactly equal:

```python
a = long[long["store"] == "A"][["date", "sales"]]
prices = pd.read_csv("prices.csv", parse_dates=["valid_from"])

exact = a.merge(prices, left_on="date", right_on="valid_from", how="left")
print(exact["price"].notna().sum())        # 5
```

5 of the 366 days have a price. `merge_asof` finds, for every row, **the
latest record on or before that date**:

```python
joined = pd.merge_asof(a, prices, left_on="date", right_on="valid_from")
print(joined[joined["date"].between("2024-03-14", "2024-03-16")])
```

```text
         date  sales valid_from  price
73 2024-03-14    327 2024-01-01   19.9
74 2024-03-15    313 2024-03-15   21.5
75 2024-03-16    426 2024-03-15   21.5
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>13 March</span><span>latest price record: <b>1 January</b> → 19.9</span></div>
    <div class="anat-row"><span>14 March</span><span>latest price record: <b>1 January</b> → 19.9</span></div>
    <div class="anat-row"><span>15 March</span><span>a new record: <b>15 March</b> → 21.5</span></div>
    <div class="anat-row"><span>16 March</span><span>latest price record: <b>15 March</b> → 21.5</span></div>
  </div>
  <figcaption>Each day looks back and finds the latest price change before it (or on the same day). A five-row price list is enough for all 366 days.</figcaption>
</figure>

14 March is still at the old price; from 15 March the new one applies.

```python
joined["revenue"] = joined["sales"] * joined["price"]
print(round(joined["revenue"].sum(), 1))       # 2562737.2
```

By default `merge_asof` looks **backwards**, so it does not use the future.
Both tables have to be sorted by date. With several series, `by="store"` does
the matching per shop.

## Joining tables of different frequencies

The targets are given monthly (`targets.csv`: `month`, `store`, `target`),
the sales daily. The way to join them is to bring the frequent one **down**
to the frequency of the sparse one:

```python
targets = pd.read_csv("targets.csv")

long["month"] = long["date"].dt.to_period("M").astype(str)
actual = long.groupby(["month", "store"])["sales"].sum().reset_index()

report = actual.merge(targets, on=["month", "store"], how="left")
report["pct"] = (report["sales"] / report["target"] * 100).round(1)
print(report[report["month"] == "2024-06"])
```

```text
      month store  sales  target   pct
17  2024-06     A   8926    9580  93.2
18  2024-06     B   4987    5400  92.4
19  2024-06     C   5794    6140  94.4
20  2024-06     D   3994    4450  89.8
```

The key is two columns: month and shop. Doing it the other way (copying the
monthly target onto days) leads to the upsampling trap of Section 05: a
target is a total and cannot be copied onto days.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| Plain `shift` / `diff` / `rolling` in the long shape | Another series' value gets mixed in | With `groupby("store")` |
| Filling every `NaN` with zero | "Absent" and "zero" get confused | By what the gap means |
| Analysing a total whose number of series changes | A break is taken for growth | Compare the same set, or flag it |
| Comparing growth with raw levels | The big series is always "ahead" | An index based at 100, or percent change |
| Taking a daily correlation for a relationship | You are measuring the weekly pattern | Remove the pattern or downsample |
| Joining a price list with `merge` | Only the change days match | `merge_asof` |
| Copying a monthly total onto a daily table | The total is counted many times over | Bring the daily one down to monthly |

## Summary

- The **long** shape has one row per (date, series). The **wide** shape has
  one column per series. `pivot` and `melt` go between them.
- The wide shape shows, as `NaN`, the missing rows that are invisible in the
  long shape.
- In the long shape every time series operation goes **with `groupby`**:
  `shift`, `diff`, `rolling`, `resample` (`pd.Grouper`).
- To compare, **index** the series or look at shares; raw levels mislead.
- `NaN` has two meanings: **closed** (zero) and **absent** (undefined).
  Decide which it is before filling.
- **`merge_asof`** brings onto each row the latest record in effect on that
  date.
- When joining different frequencies, bring the frequent one down to the
  sparse one.
