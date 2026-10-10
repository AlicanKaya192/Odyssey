`groupby` is fast, but only when it leaves the calculation to pandas' **own**
functions. Writing a `lambda` inside makes a separate Python call for each
group; the gap grows with the number of groups.

```python
import time
import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
df = pd.DataFrame({"store": rng.integers(0, 50_000, 500_000),
                   "sales": rng.uniform(0, 100, 500_000)})

start = time.perf_counter()
fast = df.groupby("store")["sales"].sum()
t_fast = time.perf_counter() - start
start = time.perf_counter()
slow = df.groupby("store")["sales"].agg(lambda s: s.sum())
t_slow = time.perf_counter() - start
print(len(fast), np.allclose(fast, slow), t_slow > 10 * t_fast)

totals = df.groupby("store")["sales"].transform("sum")
share = df["sales"] / totals
per_store = share.groupby(df["store"]).sum()
print(len(share) == len(df), round(float(per_store.mean()), 6))
```

```text
49998 True True
True 1.0
```

## What was measured?

- Half a million rows, about 50,000 stores (49,998 in the output). `sum()`
  and `agg(lambda s: s.sum())` give the same result; but the `lambda` means a
  separate Python call for each store. On this computer the gap is over
  thirty times and grows with the number of groups (with 5,000 stores it was
  a few times).
- Give the calculation by name: `"sum"`, `"mean"`, `"max"`, `"count"`,
  `"std"`, `"nunique"`, `"first"`. These run in C inside.

## transform: spread the group result back to the rows

- For "each sale's share of its store total", two steps come to mind:
  compute the group total, then join it with the rows (`merge`).
- `transform("sum")` does it in one step: the result is **as long as the
  rows**, and each row gets its own group's total. The shares add up to 1
  within each group.
- Deviation from the group mean (`df["sales"] - g.transform("mean")`), rank
  within the group (`g.rank()`), filling missing values within the group
  (`fillna` with `g.transform("mean")`) are all the same pattern.

## When is a lambda unavoidable?

If the calculation really is special (a custom ratio of two columns, a
complex rule), `apply` / `lambda` may stay. First try this: split the
calculation into columns (an intermediate column with `assign`), then use a
built-in aggregation. Most "special" calculations split this way.
