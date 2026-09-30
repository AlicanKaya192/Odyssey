## Between the two shapes

```python
wide = long.pivot(index="date", columns="store", values="sales")     # long -> wide
long = wide.reset_index().melt(id_vars="date", var_name="store",
                               value_name="sales").dropna()         # wide -> long
```

| Tool | When |
|---|---|
| `pivot` | When each (date, series) pair appears **at most once** |
| `pivot_table(..., aggfunc="sum")` | When pairs repeat; it summarises the repeats |
| `melt` | To turn a wide table into a long one |
| `stack()` / `unstack()` | The same job with index levels |

`pivot` raises when it meets a repeated pair
(`Index contains duplicate entries`). That is a good thing: the repeat
problem of Section 03 shows itself here. Resolve the repeats first, or use
`pivot_table` knowingly.

`dropna()` after `melt`: the `NaN` cells of the wide table become empty rows
in the long table; mostly they are not wanted.

## Which shape for what

| Job | Long | Wide |
|---|---|---|
| Writing to a file, a database | ✓ | |
| Many series, or a changing number | ✓ | |
| Extra columns per series (price, stock) | ✓ | |
| A feature table for machine learning | ✓ | |
| Comparing series, correlation | | ✓ |
| Plotting (one line per series) | | ✓ |
| Totals, shares, ranks across series | | ✓ |
| Seeing what is missing | | ✓ |

## Per-series operations in the long shape

```python
g = long.groupby("store")["sales"]

long["lag1"] = g.shift(1)
long["lag7"] = g.shift(7)
long["change"] = g.diff()
long["growth"] = g.pct_change()
long["ytd"] = g.cumsum()
long["ma7"] = g.transform(lambda x: x.rolling(7).mean())
long["safe_ma7"] = g.transform(lambda x: x.shift(1).rolling(7).mean())
long["z"] = g.transform(lambda x: (x - x.mean()) / x.std())
```

**Sort first.** These operations work by row order within each group:
`long = long.sort_values(["store", "date"])`.

**`shift(7)` counts rows.** Shop C has no Sunday rows; its `shift(7)` goes
back not 7 days but 7 **open days** (8 calendar days). For a lag by the
calendar, first put each shop on the full calendar:

```python
full = (long.set_index("date").groupby("store")["sales"]
        .apply(lambda x: x.asfreq("D")).reset_index())
```

## Resampling per series

```python
long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()
long.groupby(["store", pd.Grouper(key="date", freq="ME")])["sales"].agg(["sum", "mean"])
long.set_index("date").groupby("store")["sales"].resample("W").sum()
```

The first and third lines give the same result. Use `Grouper(key=...)` when
the date is a column, `resample` when it is the index.

## Operations across series in the wide shape

```python
wide.sum(axis=1)                          # each day: the total of the series
wide.mean(axis=1)                         # each day: the mean of the series
wide.div(wide.sum(axis=1), axis=0)        # each day: the share
wide.rank(axis=1, ascending=False)        # each day: the rank
wide.idxmax(axis=1)                       # each day: the highest series
wide.corr()                               # correlation between series
wide / wide.iloc[0] * 100                 # an index against the first day
wide.sub(wide.mean(axis=1), axis=0)       # deviation from the day's mean
```

`axis=1` means "along the row, across the columns". Inside `div` and `sub`,
`axis=0` means "each row by its own value".

## Gaps when adding up

| Expression | A series that is `NaN` |
|---|---|
| `wide.sum(axis=1)` | Skipped (as if 0) |
| `wide.sum(axis=1, min_count=4)` | The result is `NaN` unless all four are there |
| `wide.mean(axis=1)` | Skipped; the mean is of **the series present** |
| `wide.dropna().sum(axis=1)` | Only the days on which every series exists |

If the number of series changes over time, neither the total nor the mean is
**comparable.** There are two honest ways: work with a fixed set of series,
or use a measure that does not depend on the number of series, such as "mean
per shop".

## Hierarchy

Series are often nested: shop → city → region → total. The lower levels must
add up to the upper one. Forecast each level separately and the forecasts do
not agree (the shop forecasts do not add up to the city forecast). The name
of this problem is **hierarchical reconciliation**; the simplest fix is to
forecast the lowest level and add upwards.
