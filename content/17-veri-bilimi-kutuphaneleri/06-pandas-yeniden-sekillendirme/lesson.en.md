# Reshaping

The same data can be written in two forms. In the **wide** form each month
is a column: easy for a person to read, the way Excel reports are. In the
**long** form each measurement is a row (city, month, sales): `groupby`,
plotting libraries and models want this. Much of the time in data science
goes into moving between the two. This section covers `melt`, `pivot`,
`pivot_table`, `stack` / `unstack` and `explode`, and the silent traps of
each.

## melt: wide to long

```python
import pandas as pd

wide = pd.DataFrame({"city": ["Izmir", "Ankara"],
                     "jan": [80, 120], "feb": [95, 110]})
long = wide.melt(id_vars="city", var_name="month", value_name="sales")
print(long)
print(wide.shape, long.shape)
```

```text
     city month  sales
0   Izmir   jan     80
1  Ankara   jan    120
2   Izmir   feb     95
3  Ankara   feb    110
(2, 3) (4, 3)
```

- `id_vars` is the column(s) that stay as they are: each row's identity.
- The remaining columns (`jan`, `feb`) melt into two columns: the column's
  name goes to `var_name`, its value to `value_name`.
- 2 rows × 2 months = 4 rows. The row count multiplies by the number of
  months; that is expected, not a mistake.
- To melt only some columns, `value_vars=["jan", "feb"]`.

## pivot: long to wide

```python
import pandas as pd

long = pd.DataFrame({"city": ["Izmir", "Ankara", "Izmir", "Ankara"],
                     "month": ["jan", "jan", "feb", "feb"],
                     "sales": [80, 120, 95, 110]})
wide = long.pivot(index="city", columns="month", values="sales")
print(wide)
print(wide.columns.name, wide.index.name)
flat = wide.reset_index().rename_axis(columns=None)
print(flat.columns.tolist())
```

```text
month   feb  jan
city            
Ankara  110  120
Izmir    95   80
month city
['city', 'feb', 'jan']
```

- `pivot` is the opposite of melt: `index` gives the rows, the values of
  `columns` the column headers, `values` the cells.
- **The columns were sorted alphabetically:** `feb` came before `jan`. For
  something with a natural order like months, give the order yourself with
  `wide[["jan", "feb"]]`.
- The column axis of the result has a name (`month`); that is what shows at
  the top left. To get back to a flat table, `reset_index()` and
  `rename_axis(columns=None)`.

## A repeated pair: pivot fails

```python
import pandas as pd

long = pd.DataFrame({"city": ["Izmir", "Izmir", "Ankara"],
                     "month": ["jan", "jan", "jan"], "sales": [30, 50, 120]})
try:
    long.pivot(index="city", columns="month", values="sales")
except ValueError as error:
    print("ValueError:", error)
table = long.pivot_table(index="city", columns="month", values="sales",
                         aggfunc="sum")
print(table)
```

```text
ValueError: Index contains duplicate entries, cannot reshape
month   jan
city       
Ankara  120
Izmir    80
```

- Izmir's January appears twice (30 and 50). `pivot` cannot put two values
  in one cell and stops: "Index contains duplicate entries".
- `pivot` **rearranges**, it does not compute. If the repeats are to be
  combined with a calculation (sum, mean), the right tool is `pivot_table`:
  `aggfunc="sum"` made Izmir's January 80.
- This error often shows an unexpected repeat in the data; before blindly
  switching to `pivot_table`, look at why the repeat exists.

## pivot_table: a summary table

```python
import pandas as pd

sales = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa"],
    "month": ["jan", "feb", "jan", "jan", "feb"],
    "amount": [80, 95, 70, 50, 65],
})
table = sales.pivot_table(index="city", columns="month", values="amount",
                          aggfunc="sum", fill_value=0,
                          margins=True, margins_name="total")
print(table)
counts = pd.crosstab(sales["city"], sales["month"])
print(counts.loc["Ankara"].to_dict())
```

```text
month   feb  jan  total
city                   
Ankara    0  120    120
Bursa    65    0     65
Izmir    95   80    175
total   160  200    360
{'feb': 0, 'jan': 2}
```

- The counterpart of Excel's pivot table. `aggfunc` chooses the calculation
  (its default is **`"mean"`**; if you want a sum you have to say so).
- `fill_value=0`: a pair with no records (Ankara's February) becomes 0
  instead of `NaN`.
- `margins=True` adds row and column totals; their name is `margins_name`.
- `pd.crosstab` counts **how many times** two columns appear together:
  Ankara has 2 records in January. A shortcut to pivot_table for counting.

## stack and unstack

```python
import pandas as pd

wide = pd.DataFrame({"jan": [80, 120], "feb": [95, None]},
                    index=["Izmir", "Ankara"])
long = wide.stack()
print(type(long.index).__name__, len(long))
print(long)
back = long.unstack()
print(back.columns.tolist(), back.isna().sum().sum())
```

```text
MultiIndex 4
Izmir   jan     80.0
        feb     95.0
Ankara  jan    120.0
        feb      NaN
dtype: float64
['jan', 'feb'] 1
```

- `stack()` moves the columns down into the index's inner level: the result
  is a series with a MultiIndex. `unstack()` is the opposite; it turns the
  inner level back into columns.
- melt and pivot work with columns, stack and unstack **with the index**. If
  the data is already in the index (like the previous section's groupby
  result), these are shorter.
- In pandas 3, `stack` does **not drop** missing values: Ankara's February
  stayed as `nan`. Older versions dropped them; if the row count in an old
  example does not match, this is why. To drop them, `.dropna()`.

## explode: open a list into rows

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2], "tags": ["gift,fast", "fast"]})
orders["tags"] = orders["tags"].str.split(",")
print(orders["tags"].tolist())
rows = orders.explode("tags")
print(rows.index.tolist(), rows["tags"].tolist())
print(rows["tags"].value_counts().to_dict())
```

```text
[['gift', 'fast'], ['fast']]
[0, 0, 1] ['gift', 'fast', 'fast']
{'fast': 2, 'gift': 1}
```

- If a cell holds several values (tags, categories) separated by commas,
  first turn it into a list with `str.split(",")`.
- `explode` makes each item of the list its own row; the other columns are
  copied. After that an ordinary count or `groupby` works.
- The index is copied (`[0, 0, 1]`): a repeated label. If needed,
  `explode(..., ignore_index=True)`.

## Summary

| Direction | With columns | With the index |
|---|---|---|
| Wide to long | `melt` | `stack` |
| Long to wide | `pivot` / `pivot_table` | `unstack` |

- `pivot` stops on a repeated pair; to combine repeats use `pivot_table`
  (default calculation: mean).
- Result columns are sorted alphabetically; give the natural order yourself.
- In pandas 3, `stack` keeps missing values. Cells holding lists open into
  rows with `explode`.
