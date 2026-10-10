# pandas Index and MultiIndex

The labels to the left of a DataFrame's rows are not an ordinary column but a
separate object called the **Index**. It speeds up finding rows, does the
matching when two tables are put side by side, and causes silent mistakes when
misunderstood: `NaN` appearing when two series are added, the same label
appearing twice, a slice failing on an unsorted multi-level index. This
section explains how the Index works and the multi-level **MultiIndex**.

## Alignment: pandas adds by label

```python
import pandas as pd

jan = pd.Series({"Ankara": 120, "Izmir": 80, "Bursa": 50})
feb = pd.Series({"Izmir": 90, "Ankara": 100, "Konya": 40})
print(jan + feb)
print(jan.add(feb, fill_value=0).to_dict())
print((jan.values + feb.values).tolist())
```

```text
Ankara    220.0
Bursa       NaN
Izmir     170.0
Konya       NaN
dtype: float64
{'Ankara': 220.0, 'Bursa': 50.0, 'Izmir': 170.0, 'Konya': 40.0}
[210, 180, 90]
```

- `jan + feb` matches items not **by order** but **by label**: Ankara with
  Ankara, Izmir with Izmir. This is called **alignment**.
- A label missing on one side (Bursa only in January, Konya only in February)
  becomes `NaN`; that is also why the integers turn into `float64`.
- To count the missing side as 0, use `add(..., fill_value=0)`. The same
  parameter exists for `sub`, `mul`, `div`.
- Going down to a NumPy array with `.values` loses the labels and the addition
  happens **by order**: 210 is actually Ankara + Izmir. No error; silently
  wrong.

## set_index, loc and iloc

```python
import pandas as pd

df = pd.DataFrame({"code": ["A7", "B2", "C9"], "city": ["Izmir", "Ankara", "Bursa"],
                   "stock": [14, 3, 8]})
items = df.set_index("code")
print(items.index)
print(items.loc["B2", "stock"], items.iloc[1, 1])
print(items.loc[["C9", "A7"], "city"].tolist())
print(items.reset_index().columns.tolist())
```

```text
Index(['A7', 'B2', 'C9'], dtype='str', name='code')
3 3
['Bursa', 'Izmir']
['code', 'city', 'stock']
```

- `set_index("code")` moves a column into the index; it leaves the columns.
  The Index has a name (`name='code'`) and a type (text is `str` in pandas 3).
- `loc` selects **by label**, `iloc` **by position**. `items.iloc[1, 1]` is
  the second row, second column: since `code` is no longer a column, the
  second column is `stock`.
- Given a list, `loc` returns the rows in that order.
- `reset_index()` turns the index back into a column and numbers the rows 0,
  1, 2 again.

## Repeated labels

```python
import pandas as pd

raw = pd.DataFrame({"day": ["mon", "tue", "mon"], "amount": [10, 20, 30]})
sales = raw.set_index("day")
print(sales.index.is_unique, sales.index.duplicated().tolist())
one, two = sales.loc["tue", "amount"], sales.loc["mon", "amount"]
print(type(one).__name__, two.tolist())
try:
    sales.reindex(["mon", "tue", "wed"])
except ValueError as error:
    print("ValueError:", error)
print(sales.groupby(level="day")["amount"].sum().to_dict())
```

```text
False [False, False, True]
int64 [10, 30]
ValueError: cannot reindex on an axis with duplicate labels
{'mon': 40, 'tue': 20}
```

- An Index **does not have to be unique**. `is_unique` and `duplicated()`
  check this.
- The danger: `loc` with one label sometimes returns **a single value**
  (`tue` → `int64`), sometimes **a series** (`mon` → two rows). Code that
  expects one value one day gets a series the next.
- `reindex` does not work on repeated labels. The fix is usually to combine
  the repeats: `groupby(level="day").sum()`.
- For a key that must be unique, `set_index(..., verify_integrity=True)`
  fails at once if there are repeats.

## MultiIndex: a two-level label

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa", "Bursa"],
    "year": [2024, 2025, 2024, 2025, 2024, 2025],
    "sales": [80, 95, 120, 110, 50, 65],
})
m = df.set_index(["city", "year"]).sort_index()
print(m.index.names, m.index.nlevels)
print(m)
print(m.loc[("Izmir", 2025), "sales"])
print(m.loc["Ankara", "sales"].to_dict())
```

```text
['city', 'year'] 2
             sales
city   year       
Ankara 2024    120
       2025    110
Bursa  2024     50
       2025     65
Izmir  2024     80
       2025     95
95
{2024: 120, 2025: 110}
```

- When `set_index` takes two columns, each row's label becomes a **tuple**:
  `("Izmir", 2025)`. The levels are named `city` and `year`.
- On screen the outer level is not repeated; it is left blank for easier
  reading.
- A full label is given as a tuple: `loc[("Izmir", 2025)]`.
- Given only the outer level, all the years of that city come back and the
  outer level is dropped: `loc["Ankara"]` is a series labelled by year.

## Selecting from an inner level: xs and IndexSlice

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa", "Bursa"],
    "year": [2024, 2025, 2024, 2025, 2024, 2025],
    "sales": [80, 95, 120, 110, 50, 65],
})
m = df.set_index(["city", "year"]).sort_index()
print(m.xs(2025, level="year")["sales"].to_dict())
idx = pd.IndexSlice
print(m.loc[idx["Ankara":"Bursa", 2024], "sales"].tolist())
print(m.index.get_level_values("city").unique().tolist())
print(m.swaplevel().sort_index().index[:3].tolist())
```

```text
{'Ankara': 110, 'Bursa': 65, 'Izmir': 95}
[120, 50]
['Ankara', 'Bursa', 'Izmir']
[(2024, 'Ankara'), (2024, 'Bursa'), (2024, 'Izmir')]
```

- `loc` looks at the outer level first. To select from an **inner** level,
  such as "2025 for every city", use `xs(2025, level="year")`.
- To slice on both levels at once, use `pd.IndexSlice`: `idx["Ankara":"Bursa",
  2024]` is the 2024 rows of the cities from Ankara to Bursa (inclusive).
- `get_level_values("city")` gives one level's labels row by row (with
  repeats); `unique()` gives the distinct ones.
- `swaplevel()` swaps the levels; without a `sort_index()` afterwards the
  years stay mixed.

## An unsorted MultiIndex

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Ankara", "Izmir", "Ankara"],
    "year": [2025, 2024, 2024, 2025],
    "sales": [95, 120, 80, 110],
})
m = df.set_index(["city", "year"])
print(m.index.is_monotonic_increasing)
try:
    m.loc[("Ankara", 2024):("Izmir", 2024)]
except Exception as error:
    print(type(error).__name__ + ":", error)
s = m.sort_index()
print(s.index.is_monotonic_increasing)
print(s.loc[("Ankara", 2025):("Izmir", 2024), "sales"].tolist())
```

```text
False
UnsortedIndexError: 'Key length (2) was greater than MultiIndex lexsort depth (0)'
True
[110, 80]
```

- To slice a range, pandas has to find "where it starts, where it ends"; this
  is only possible on a **sorted** index.
- On an unsorted MultiIndex a slice raises `UnsortedIndexError`. "lexsort
  depth (0)" in the message means "no level is sorted".
- The fix is one line: `sort_index()`. Looking up a single label is also
  faster on a sorted index (binary search), so sorting right after building a
  MultiIndex is a good habit.

## The MultiIndex that comes out of groupby

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa", "Bursa"],
    "year": [2024, 2025, 2024, 2025, 2024, 2025],
    "sales": [80, 95, 120, 110, 50, 65],
})
g = df.groupby(["city", "year"])["sales"].sum()
print(type(g.index).__name__, g.index.names)
print(g.groupby(level="city").sum().to_dict())
print(g.unstack())
print(g.reset_index().head(2))
```

```text
MultiIndex ['city', 'year']
{'Ankara': 230, 'Bursa': 115, 'Izmir': 175}
year    2024  2025
city              
Ankara   120   110
Bursa     50    65
Izmir     80    95
     city  year  sales
0  Ankara  2024    120
1  Ankara  2025    110
```

- A `groupby` on two columns gives a series with a **MultiIndex**. This is
  where most people first meet a MultiIndex.
- To total again over one level, use `groupby(level="city")`.
- `unstack()` turns the inner level (`year`) into columns: the long table
  becomes a wide one. It comes in detail in the reshaping section.
- `reset_index()` turns both levels into columns; the shortest way back to a
  flat table.

## Summary

- pandas operations **align by label**; an unmatched label becomes `NaN`.
  `.values` drops the labels and computes by order.
- `loc` is label, `iloc` is position. `set_index` / `reset_index` move between
  column and index.
- A repeated label changes what `loc` returns; check with `is_unique`.
- MultiIndex: a full label as a tuple, an inner level with `xs`, a slice on
  two levels with `IndexSlice`. `sort_index()` before slicing.
