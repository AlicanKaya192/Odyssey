# pandas Performance

Two pandas programs that give the same result can differ in speed by hundreds
of times. The difference almost always comes from the same place: a Python
loop row by row, or a single operation on the whole column? This section
measures that difference and covers writing conditions without loops, pandas
3's Copy-on-Write rule, choosing types for memory and readable chained code.
Reading very large files piece by piece is the subject of the **Big Data**
path.

## A loop, apply and a vectorised operation

```python
import time
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
df = pd.DataFrame({"price": rng.uniform(1, 100, 20_000),
                   "qty": rng.integers(1, 10, 20_000)})

start = time.perf_counter()
total = [row["price"] * row["qty"] for _, row in df.iterrows()]
t_iter = time.perf_counter() - start

start = time.perf_counter()
total2 = df.apply(lambda row: row["price"] * row["qty"], axis=1)
t_apply = time.perf_counter() - start

start = time.perf_counter()
total3 = df["price"] * df["qty"]
t_vec = time.perf_counter() - start

print(np.allclose(total, total3), np.allclose(total2, total3))
print(t_iter > 50 * t_vec, t_apply > 20 * t_vec)
```

```text
True True
True True
```

- All three ways give the same result. The times on this computer: `iterrows`
  about 0.2 seconds, `apply(axis=1)` about 0.06 seconds, the vectorised
  product under a thousandth. The exact numbers change from machine to
  machine; the ratio of **hundreds of times** does not.
- `iterrows` builds a new Series object for every row; that is the real cost.
- `apply(axis=1)` is shorter to write but still calls a Python function row
  by row inside. The source of the "I wrote it in pandas, so it is fast"
  misconception.
- `df["price"] * df["qty"]` hands the work to NumPy: the loop runs in C. The
  rule: first try writing it **with columns**.

## Conditions: np.where and np.select

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"qty": [1, 12, 5, 30], "price": [10.0, 8.0, 9.0, 7.5]})
df["size"] = np.where(df["qty"] >= 10, "bulk", "single")
rules = [df["qty"] >= 25, df["qty"] >= 10]
df["discount"] = np.select(rules, [0.2, 0.1], default=0.0)
df["total"] = df["qty"] * df["price"] * (1 - df["discount"])
print(df)
```

```text
   qty  price    size  discount  total
0    1   10.0  single       0.0   10.0
1   12    8.0    bulk       0.1   86.4
2    5    9.0  single       0.0   45.0
3   30    7.5    bulk       0.2  180.0
```

- Most "if this, then that" code written with `apply` can be written without
  a loop.
- `np.where(condition, if_true, if_false)`: two choices.
- `np.select(conditions, values, default=...)`: more than two choices. The
  conditions are tried **in order**, the first that holds wins: 30 items are
  both `>= 25` and `>= 10`, but got `0.2`. That is why the narrowest
  condition is written first.

## Copy-on-Write: chained assignment does nothing

```python
import warnings
import pandas as pd

df = pd.DataFrame({"city": ["Izmir", "Ankara", "Bursa"], "stock": [5, 0, 3]})
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df[df["stock"] == 0]["stock"] = 10
print(df["stock"].tolist(), type(caught[0].message).__name__)
part = df[df["stock"] > 0]
part["stock"] = 99
print(df["stock"].tolist(), part["stock"].tolist())
df.loc[df["stock"] == 0, "stock"] = 10
print(df["stock"].tolist())
```

```text
[5, 0, 3] ChainedAssignmentError
[5, 0, 3] [99, 99]
[5, 10, 3]
```

- pandas 3 uses **Copy-on-Write**: every table derived from another (a
  filter, a column selection) behaves as a **separate copy**. The real copy
  is made only when one of them is changed; hence the name.
- `df[filter]["stock"] = 10` is two steps: first the filter makes a new
  table, the assignment goes to that table. `df` does not change; pandas
  gives a `ChainedAssignmentError` warning.
- `part = df[...]` then `part[...] = 99`: only `part` changes, `df` stays as
  it was. The confusion of old pandas' `SettingWithCopyWarning` is over; the
  rule is simple.
- To change the original table, **in one step**: `df.loc[row_condition,
  "column"] = value`.

## Choosing types for memory

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(1)
n = 1_000_000
df = pd.DataFrame({
    "store": rng.choice(["Izmir", "Ankara", "Bursa"], n),
    "qty": rng.integers(0, 100, n),
    "price": rng.uniform(1, 50, n),
})
before = df.memory_usage(deep=True).sum() / 1e6
small = df.assign(store=df["store"].astype("category"),
                  qty=pd.to_numeric(df["qty"], downcast="unsigned"),
                  price=df["price"].astype("float32"))
after = small.memory_usage(deep=True).sum() / 1e6
print(small.dtypes.astype(str).tolist())
print(round(before, 1), round(after, 1))
print(abs(small["price"].sum() - df["price"].sum()) / df["price"].sum() < 1e-6)
```

```text
['category', 'uint8', 'float32']
29.3 6.0
True
```

- The defaults are generous: integers `int64` (8 bytes), decimals `float64`.
  For a count between 0 and 99, 1 byte (`uint8`) is enough.
- `pd.to_numeric(..., downcast="unsigned")` looks at the values and picks
  the smallest type that fits. The three different store names are coded
  with `category`.
- Over a million rows 29.3 MB became 6.0 MB. A smaller table is also
  processed faster: work that did not fit in memory now fits.
- `float32` keeps about 7 digits of precision; the relative difference in
  the total stayed under one in a million. Where every cent matters, like
  money, keep `float64`.

## query and chaining

```python
import pandas as pd

df = pd.DataFrame({"city": ["Izmir", "Ankara", "Bursa", "Izmir"],
                   "qty": [5, 12, 3, 20], "price": [10.0, 8.0, 9.0, 7.5]})
limit = 4
a = df[(df["qty"] > limit) & (df["city"] == "Izmir")]
b = df.query("qty > @limit and city == 'Izmir'")
print(a.equals(b), b.index.tolist())
result = (
    df.assign(total=lambda d: d["qty"] * d["price"])
      .query("total > 40")
      .groupby("city")["total"].sum()
      .sort_values(ascending=False)
)
print(result.to_dict())
```

```text
True [0, 3]
{'Izmir': 200.0, 'Ankara': 96.0}
```

- `query` writes the filter as text: `and` instead of a crowd of brackets and
  `&`. A Python variable is referenced with `@`. The result is exactly the
  same as the bracket filter.
- `assign(total=lambda d: ...)` adds a new column **inside the chain**; `d`
  is the table at that step. No intermediate variables (`df2`, `df3`) are
  needed and the original `df` does not change.
- A chain in brackets reads each step on its own line: "add the total → take
  those over 40 → total by city → sort". When debugging, commenting out a
  line is enough.

## Summary

- Write with columns first; `iterrows` and `apply(axis=1)` are row-by-row
  Python and hundreds of times slower.
- Conditions with `np.where` (two choices) and `np.select` (many choices, the
  first that holds wins).
- pandas 3: a derived table behaves as a separate copy. To change, in one
  step: `df.loc[condition, column] = value`.
- `downcast`, `category`, `float32` shrink memory; mind the precision.
- Chains with `query` and `assign`: readable, without intermediate variables.
