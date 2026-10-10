# Text and Categorical Data

Hand-entered text columns are messy: " Izmir", "izmir" and "IZMIR" count as
three different cities, and codes hold information that needs to be taken
apart. On the other hand, in a table of a million rows a column with only
three different values stores the same text over and over in every row. These
are the two subjects of this section: cleaning and taking apart text in bulk
with `.str`, and holding repeated values with little memory and in the right
order with the `category` type.

## .str: the whole column at once

```python
import pandas as pd

names = pd.Series(["  Izmir", "izmir ", "IZMIR", "Ankara", None])
print(names.dtype, names.nunique())
clean = names.str.strip().str.title()
print(clean.tolist(), clean.nunique())
print(clean.str.len().tolist())
```

```text
str 4
['Izmir', 'Izmir', 'Izmir', 'Ankara', nan] 2
[5.0, 5.0, 5.0, 6.0, nan]
```

- Python's text methods (`strip`, `lower`, `title`, `replace`, `split`) work
  on a column through `.str`; no loop needed.
- Before cleaning there were 4 different cities, after it 2. Without this
  cleaning before grouping, Izmir's sales get split into three parts.
- A missing value (`None`) does not raise an error, it stays missing. That is
  why `str.len()` returns decimals: `NaN` cannot be held in an integer.
- In pandas 3 the type of a text column is `str`.

## contains and missing values

```python
import pandas as pd

notes = pd.Series(["late delivery", "Delivery OK", None, "broken box"])
print(notes.str.contains("delivery").tolist())
print(notes.str.contains("delivery", case=False).tolist())
print(notes.str.contains("late|broken").tolist())
old = notes.astype(object)
try:
    old[old.str.contains("delivery")]
except ValueError as error:
    print("ValueError:", error)
print(len(old[old.str.contains("delivery", na=False)]))
```

```text
[True, False, False, False]
[True, True, False, False]
[True, False, False, True]
ValueError: Cannot mask with non-boolean array containing NA / NaN values
1
```

- `contains` is case-sensitive; `case=False` finds both.
- The pattern is a **regular expression** by default: `"late|broken"` means
  "late or broken". To search for characters like dots and brackets
  literally, `regex=False`.
- In pandas 3's `str` type a missing value returns `False`. In the old type
  (`object`, old pandas or a column coming from elsewhere) the result holds
  `None` and cannot be used as a filter: "Cannot mask with non-boolean
  array". `na=False` is safe in both cases.

## extract: taking apart with a regular expression

```python
import pandas as pd

codes = pd.Series(["TR-34-0012", "TR-06-0450", "DE-11-0007", "bad"])
pattern = r"(?P<country>[A-Z]{2})-(?P<region>\d{2})-(?P<num>\d{4})"
parts = codes.str.extract(pattern)
print(parts)
print(parts["num"].astype("Int64").tolist())
print(codes.str.split("-", expand=True).shape)
print(codes.str.replace(r"\d", "#", regex=True).tolist())
```

```text
  country region   num
0      TR     34  0012
1      TR     06  0450
2      DE     11  0007
3     NaN    NaN   NaN
[12, 450, 7, <NA>]
(4, 3)
['TR-##-####', 'TR-##-####', 'DE-##-####', 'bad']
```

- `str.extract` makes each **group** of the regular expression a column;
  `?P<name>` names the column. A row that does not fit the pattern (`bad`)
  is `NaN` in every column.
- The extracted parts are text; if `0012` is to be a number,
  `astype("Int64")` (capital I: an integer that can hold a missing value as
  `<NA>`).
- `split("-", expand=True)` opens the parts into columns; shorter than
  extract when the structure is regular.
- `replace(..., regex=True)` replaces every place matching the pattern.

## category: repeated values

```python
import pandas as pd

cities = pd.Series(["Izmir", "Ankara", "Izmir", "Bursa"] * 250_000)
as_cat = cities.astype("category")
print(len(cities), as_cat.cat.categories.tolist())
print(as_cat.cat.codes[:4].tolist(), as_cat.cat.codes.dtype)
before = cities.memory_usage(deep=True) / 1e6
after = as_cat.memory_usage(deep=True) / 1e6
print(round(before, 1), round(after, 1), after < before / 5)
```

```text
1000000 ['Ankara', 'Bursa', 'Izmir']
[2, 0, 2, 1] int8
13.3 1.0 True
```

- `category` stores each different value **once** (`categories`) and keeps
  only a small **code** in each row: Ankara 0, Bursa 1, Izmir 2. The code's
  type is `int8`, that is 1 byte per row.
- Over a million rows the memory dropped from 13.3 to 1.0 MB. The gain is
  large when the number of different values is **small** compared to the
  number of rows; turning a column where every row differs (name, e-mail)
  into a category gains nothing.
- Grouping and sorting also get faster since they work on the codes.

## An ordered category

```python
import pandas as pd

sizes = pd.Series(["M", "S", "XL", "M", "L"])
print(sorted(sizes.unique()))
size_type = pd.CategoricalDtype(["S", "M", "L", "XL"], ordered=True)
sized = sizes.astype(size_type)
print(sized.sort_values().tolist())
print((sized >= "L").tolist(), sized.max())
print(sizes.astype(size_type).value_counts(sort=False).to_dict())
```

```text
['L', 'M', 'S', 'XL']
['S', 'M', 'M', 'L', 'XL']
[False, False, True, False, True] XL
{'S': 1, 'M': 2, 'L': 1, 'XL': 1}
```

- Text sorts alphabetically: `L, M, S, XL`. Meaningless for sizes.
- With `CategoricalDtype(..., ordered=True)` **you** give the order: S < M <
  L < XL. Now sorting, the `>=` comparison and `max()` work by size.
- `value_counts(sort=False)` gives the categories in their own order; so the
  axis comes out in the right order in reports and charts.
- The same pattern for every ordered class: a satisfaction survey ("bad <
  fair < good"), education level, priority.

## cut and qcut: turning numbers into classes

```python
import pandas as pd

ages = pd.Series([15, 22, 37, 45, 61, 70])
bins = [0, 18, 40, 65, 120]
groups = pd.cut(ages, bins=bins, labels=["child", "young", "middle", "senior"])
print(groups.tolist())
print(groups.value_counts(sort=False).to_dict())
print(pd.cut(ages, bins=[0, 18, 40]).isna().sum())
quart = pd.qcut(ages, q=3, labels=["low", "mid", "high"])
print(quart.tolist())
```

```text
['child', 'young', 'young', 'middle', 'middle', 'senior']
{'child': 1, 'young': 2, 'middle': 2, 'senior': 1}
3
['low', 'low', 'mid', 'mid', 'high', 'high']
```

- `cut` groups numbers by **the limits you give**. The intervals are closed
  on the right: `(18, 40]` excludes 18 and includes 40. The result is an
  ordered category.
- A value outside the limits becomes `NaN`: there was no limit for 45, 61
  and 70, so 3 values were lost. Keep the last limit wide.
- `qcut` chooses the limits **from the data itself**: so that each group has
  about the same number of people (2 each here).

## Summary

- `.str` applies text methods to the whole column; clean with `strip`,
  `lower` / `title` before grouping.
- `contains` uses regular expressions; `na=False` for missing values in the
  old type.
- `str.extract` opens the groups into columns.
- `category`: little memory for a few different values; an ordered category
  lets you give the order.
- `cut` with your limits, `qcut` so that the groups are equal in size.
