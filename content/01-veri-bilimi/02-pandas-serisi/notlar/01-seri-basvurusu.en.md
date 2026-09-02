# Series Reference

Everything assumes `import pandas as pd`.

## Creating

| Written as | What it does |
|---|---|
| `pd.Series([1, 2, 3])` | A Series from a list; index 0, 1, 2 |
| `pd.Series([1, 2], index=["a", "b"])` | A labelled index |
| `pd.Series({"a": 1, "b": 2})` | From a dictionary; the keys become the index |
| `pd.Series(5, index=["a", "b"])` | The same value everywhere |
| `pd.Series(numpy_array)` | From a NumPy array |

## Attributes

| Written as | What it gives |
|---|---|
| `s.index` | The labels |
| `s.values` | The values (as a NumPy array) |
| `s.dtype` | The type of the values |
| `s.size` | Total number of cells (**including empty ones**) |
| `s.count()` | Number of **filled** cells |
| `s.name` | The Series' name |
| `s.empty` | Whether it is empty |

If `size` and `count()` differ, there are missing values. This is the first
thing to check when you look at a Series.

## Selecting

| Written as | What it selects |
|---|---|
| `s["Ada"]` | A single value by label |
| `s[["Ada", "Mina"]]` | Several labels |
| `s.iloc[0]` | The first element by **position** |
| `s.iloc[1:3]` | A slice by position |
| `s.loc["Ada"]` | By label (the explicit form) |
| `s[s > 80]` | By condition |
| `s.head(3)` / `s.tail(3)` | The first / last three |

When the index is made of numbers, `s[0]` is ambiguous: is that a label or a
position? That is why `loc` (label) and `iloc` (position) exist — the subject
of the next section.

## Aggregation

| Written as | What it gives |
|---|---|
| `s.sum()` | The total |
| `s.mean()` | The mean |
| `s.median()` | The median |
| `s.std()` | The standard deviation |
| `s.min()` / `s.max()` | The extremes |
| `s.idxmin()` / `s.idxmax()` | The **label** of the smallest / largest |
| `s.describe()` | Eight numbers at once |
| `s.cumsum()` | Running total |

**All of them skip missing values.** NumPy did not; there `mean()` gave `nan`
because of a single `nan`.

NumPy's `argmax` gave a position; pandas's `idxmax` gives a **label**:
`scores.idxmax()` tells you directly who scored highest.

## Missing values

| Written as | What it does |
|---|---|
| `s.isna()` | Which cells are empty (`True`/`False`) |
| `s.notna()` | The opposite |
| `s.isna().sum()` | How many are empty |
| `s.dropna()` | A **new Series** with the empty ones removed |
| `s.fillna(0)` | A **new Series** with the gaps set to zero |
| `s.fillna(s.mean())` | Filled with the mean |
| `s.ffill()` | Fill a gap with the value above it |
| `s.bfill()` | Fill with the value below it |

`fillna` and `dropna` **do not modify** the original Series; if you do not
assign the result it is lost.

You may see `fillna(method="ffill")` in older documentation; it was
**removed in pandas 3.0** and `ffill()` and `bfill()` are separate methods
now.

## Categorical values

| Written as | What it gives |
|---|---|
| `s.value_counts()` | How many of each value, most first |
| `s.value_counts(normalize=True)` | The same as proportions |
| `s.unique()` | The distinct values, **in order of appearance** |
| `s.nunique()` | How many distinct values |
| `s.isin(["Ankara", "Izmir"])` | Whether it is one of the listed values |

`np.unique` sorted the result; `Series.unique()` **does not** — it keeps the
order of first appearance. Two functions with the same name in two libraries
behave differently.

## Converting and sorting

| Written as | What it does |
|---|---|
| `s.astype(int)` | Changes the type |
| `s.sort_values()` | A **new Series** sorted by value |
| `s.sort_values(ascending=False)` | Largest first |
| `s.sort_index()` | Sorted by label |
| `s.tolist()` | Converts to a Python list |
| `s.to_dict()` | Converts to a dictionary |
| `s.reset_index(drop=True)` | Renumbers the index from 0 |

## An operation on every element

| Written as | What it does |
|---|---|
| `s * 2` | Vectorised — the fastest and the preferred way |
| `s.apply(function)` | Applies the function to every element |
| `s.map({"a": 1, "b": 2})` | Replaces values using a dictionary |
| `s.round(2)` | Rounds |

`apply` is flexible but slow: there is a Python loop behind it. If there is a
vectorised equivalent, use that.

## Text Series

| Written as | What it does |
|---|---|
| `s.str.lower()` | Everything to lower case |
| `s.str.strip()` | Removes leading and trailing spaces |
| `s.str.contains("An")` | Whether it contains something |
| `s.str.len()` | The lengths |
| `s.str.split(",")` | Splits |

None of these work without `.str`: there is no `s.lower()`, because `s` is
not a string but a Series of strings.
