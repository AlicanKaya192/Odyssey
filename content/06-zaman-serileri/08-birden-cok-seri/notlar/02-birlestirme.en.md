## Three kinds of join

| Tool | Matching | When |
|---|---|---|
| `merge` | Keys are **exactly** equal | Two tables at the same frequency; keys such as month and shop |
| `merge_asof` | The **nearest** earlier (or later) record | A price list, an exchange rate, a settings change, readings arriving at different times |
| `join` / `concat(axis=1)` | Alignment on the index | Series with the same index side by side |

## `merge_asof`

```python
pd.merge_asof(left, right, on="date")                    # a date column of the same name
pd.merge_asof(left, right, left_on="date", right_on="valid_from")
pd.merge_asof(left, right, on="date", by="store")        # per series
pd.merge_asof(left, right, on="time", tolerance=pd.Timedelta("10min"))
pd.merge_asof(left, right, on="time", direction="nearest")
```

| Parameter | What it does |
|---|---|
| `direction="backward"` | The latest record on or **before** that date (the default) |
| `direction="forward"` | The first record on or **after** that date; uses the future |
| `direction="nearest"` | Whichever is closer; may use the future |
| `tolerance=` | Do not match a record further away than this; leave `NaN` |
| `by=` | Do the matching separately for each value of this column |
| `allow_exact_matches=False` | Do not match the very same moment; strictly earlier |

**Both tables must be sorted by the key column.** Otherwise you get
`left keys must be sorted`.

**`backward` for forecasting.** `forward` and `nearest` can bring onto a row
a record that came after it; fine in analysis, leakage when building
features.

**`tolerance` keeps stale data out.** If a sensor has sent nothing for two
days, `merge_asof` still brings the value from two days ago. With `tolerance`
you can say "anything older than this is not valid".

**`allow_exact_matches=False`** prevents using a record that arrived at the
same moment as the event. In daily data, if the answer to "was today's price
known before today's sales?" is no, use this.

## Different frequencies

| Case | Way |
|---|---|
| Daily sales + a monthly target | Bring the daily one **down** to months, then `merge` |
| Daily sales + a monthly price list (a level) | **Carry** the price onto days: `merge_asof` or `ffill` |
| Hourly consumption + daily temperature | Either bring consumption down to days or carry temperature onto hours (knowingly) |
| Two irregular sensors | `resample` both onto the same grid, then join |

The general rule comes from Section 05: **a total goes down, a level is
carried up.**

## Matching the same period

Mind the labels when joining monthly tables:

```python
a.index = a.index.to_period("M")     # 2024-03-31 -> 2024-03
b.index = b.index.to_period("M")     # 2024-03-01 -> 2024-03
a.to_frame("a").join(b.to_frame("b"))
```

Joining two tables directly, one labelled at month end and the other at month
start, matches no rows. Turning both into periods is the sturdiest way.

## Checking after a join

```python
print(len(left), len(joined))                 # did the number of rows change?
print(joined["price"].isna().sum())           # how many rows did not match?
print(joined["date"].duplicated().sum())      # did rows multiply?
```

- **If the number of rows went up**, the key repeats in the right table; each
  left row matched several times and the totals are inflated.
- **If there are many `NaN` values**, the keys do not agree: a type
  difference (text and date), a label difference (month start and month end),
  whitespace or letter case.
- `merge(..., validate="many_to_one")` checks the relationship you expect; it
  raises if the right side has repeats.

## A lagged relationship between series

To see whether one series tells you about another **in advance**, shift one
and look at the correlation:

```python
for k in (0, 1, 7):
    print(k, round(wide["A"].corr(wide["B"].shift(k)), 3))
```

This is called cross-correlation. A high value is no proof of causation: both
series may simply follow the same calendar (weekends, holidays). Section 18
takes it up together with external variables.
