## Building it

```python
s = pd.read_csv("f.csv", index_col="date", parse_dates=True)["value"]
s = s.sort_index()

df = df.set_index("date").sort_index()   # from column to index
df = df.reset_index()                    # from index back to column
```

## Selecting

| You write | You get |
|---|---|
| `s.loc["2024-03-09"]` | One day (a single value) |
| `s.loc["2024-03"]` | All of March 2024 |
| `s.loc["2024"]` | All of 2024 |
| `s.loc["2024-03-04":"2024-03-10"]` | Both ends **included** |
| `s.loc["2024-01":"2024-03"]` | From the start of January to the end of March |
| `s.loc[:"2024-06-30"]` | From the start up to that day |
| `s.loc["2024-12-25":]` | From that day to the end |
| `s.loc["2024-03-15 08:00":"2024-03-15 12:00"]` | A range of hours (hourly data) |
| `s.iloc[-7:]` | The last 7 **rows** (whatever their dates) |
| `s.truncate(before="2024-12-01")` | Drop everything before that date |
| `s[s.index.dayofweek >= 5]` | Weekends |
| `s[s.index.month == 12]` | Every December |
| `s.between_time("08:00", "18:00")` | Those hours of every day |
| `s.at_time("18:00")` | Exactly that time of every day |

**One day versus a range:** in daily data `s.loc["2024-03-09"]` gives a single
number; in hourly data the same expression gives that day's 24 rows.

## Properties of the index

```python
s.index.min(), s.index.max()
s.index[-1] - s.index[0]              # total span
s.index.year, s.index.month, s.index.day
s.index.dayofweek, s.index.day_name()
s.index.hour                          # in hourly data
s.index.normalize()                   # zero the times
s.index.is_monotonic_increasing       # is it in order
s.index.is_unique                     # are there no repeats
s.index.freq                          # the frequency (may be None)
pd.infer_freq(s.index)                # a guess at the frequency
```

## The cleaning recipe

```python
s = pd.read_csv("f.csv", index_col="date", parse_dates=True)["value"]

# 1. Sort
s = s.sort_index()

# 2. Repeats
print(s.index.duplicated().sum())
s = s.groupby(level=0).sum()          # or .last() / .mean() / ~duplicated()

# 3. Gaps
full = pd.date_range(s.index.min(), s.index.max(), freq="D")
print(full.difference(s.index))

# 4. Put it on the calendar
s = s.asfreq("D")
print(s.isna().sum())
```

The order of the steps matters: `asfreq` raises while there are repeats, and
slicing does not work while the index is unsorted.

## Resolving repeats

| Method | When |
|---|---|
| `s.groupby(level=0).sum()` | The values are parts of a total (sales, counts) |
| `s.groupby(level=0).mean()` | Several measurements of the same moment (temperature) |
| `s.groupby(level=0).last()` | A later correction is the valid one |
| `s.groupby(level=0).first()` | The first record is the valid one |
| `s[~s.index.duplicated(keep="first")]` | The very same row arrived twice |

## Measuring the gaps

```python
gaps = s.index.to_series().diff()
print(gaps.value_counts())     # 1 day: 352, 2 days: 3, 3 days: 1, 4 days: 1
print(gaps.max())              # the longest gap
```

If the difference between two rows is more than 1 day, days are missing in
between. A difference of 4 days means 3 missing days.

## `asfreq`, `reindex`, `resample`

| Tool | What it does |
|---|---|
| `s.asfreq("D")` | Puts the series on the full calendar, gaps become `NaN` |
| `s.asfreq("D", fill_value=0)` | Fills the gaps with a constant |
| `s.reindex(full)` | Puts it on any index you give |
| `s.resample("D").sum()` | **Changes** the frequency and aggregates (Section 05) |

`asfreq` does not change values; it only opens rows. `resample` groups and
applies an operation; the two should not be confused.
