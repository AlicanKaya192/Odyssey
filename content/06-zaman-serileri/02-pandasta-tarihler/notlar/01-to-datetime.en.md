## `pd.to_datetime` parameters

| Parameter | What it does | When |
|---|---|---|
| `format="%d.%m.%Y"` | States the format explicitly | **Always**, if the date is not ISO |
| `dayfirst=True` | Puts the day first in an ambiguous date | When there is no single format; pointless with `format` |
| `errors="coerce"` | Turns what cannot be read into `NaT` | When broken rows are expected; then count them |
| `errors="raise"` | Raises on what cannot be read (the default) | When the data has to be clean |
| `utc=True` | Makes the result UTC-aware | When mixed offsets arrive, and for Unix time |
| `unit="s"` / `"ms"` | Reads a number as Unix time | When the column is numeric |
| `format="ISO8601"` | Accepts every flavour of ISO | When some rows have a time and some do not |
| `format="mixed"` | Guesses the format row by row | A last resort; see the warning below |

## A warning about `format="mixed"`

Each row is guessed separately, so it is slow and **unreliable**. Together
with `dayfirst=True` it even flips an ISO date:

```python
pd.to_datetime(pd.Series(["2024-03-09", "09.03.2024"]),
               format="mixed", dayfirst=True)
# 2024-09-03, 2024-03-09    the ISO row was read wrongly
```

For a column with mixed formats, the safer way is to split the rows by format
and read each group with its own `format`:

```python
iso = dates.str.match(r"\d{4}-\d{2}-\d{2}")
result = pd.Series(pd.NaT, index=dates.index)
result[iso] = pd.to_datetime(dates[iso], format="%Y-%m-%d")
result[~iso] = pd.to_datetime(dates[~iso], format="%d.%m.%Y")
```

## While reading the file

```python
pd.read_csv("f.csv", parse_dates=["date"])                       # an ISO column
pd.read_csv("f.csv", parse_dates=["date"], date_format="%d.%m.%Y")   # with a format
pd.read_csv("f.csv", parse_dates=["date"], index_col="date")     # straight into the index
```

If `read_csv` cannot parse it, it **does not raise**; it leaves the column as
text. Check `df.dtypes` after reading.

## A checklist after converting

```python
df["date"].dtype                 # is it datetime64[...]?
df["date"].isna().sum()          # how many NaT?
df["date"].min(), df["date"].max()   # does the range make sense?
df["date"].dt.month.value_counts().sort_index()   # are the months balanced?
df["date"].is_monotonic_increasing   # is it in order?
df["date"].duplicated().sum()    # any repeats?
```

Looking at the months gives away a day-month mix-up: if the real data covers
four months and the result is spread across twelve, day and month were
swapped.

## Working with `NaT`

| Operation | Result |
|---|---|
| `pd.NaT == pd.NaT` | `False` |
| `pd.NaT > pd.Timestamp("2024-01-01")` | `False` |
| `pd.isna(pd.NaT)` | `True` |
| `s.min()`, `s.max()`, `s.mean()` | `NaT` is skipped |
| date - `NaT` | `NaT` |
| `s.dt.month` (a NaT row) | `NaN`; the column becomes float |

The last row often surprises: on a column containing `NaT`, `dt.month` gives
floats such as `3.0`. After `dropna()` it goes back to integers.

## When writing

```python
df.to_csv("out.csv", index=False)                          # writes ISO
df.to_csv("out.csv", index=False, date_format="%Y-%m-%d")  # without the time
df["date"].dt.strftime("%d.%m.%Y")                         # to text (for a report)
```

The result of `strftime` is **text**; no date operation works on it
afterwards. Use it as the very last step, right before writing the report.
