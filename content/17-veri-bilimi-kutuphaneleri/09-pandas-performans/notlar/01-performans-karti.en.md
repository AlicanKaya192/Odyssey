## From slow to fast

| Slow | Fast |
|---|---|
| `for _, row in df.iterrows()` | `df["a"] * df["b"]` |
| `df.apply(f, axis=1)` | a column operation or `np.where` / `np.select` |
| `g.agg(lambda s: s.sum())` | `g.sum()` or `g.agg("sum")` |
| group total + `merge` | `g.transform("sum")` |
| `concat` in a loop | collect pieces in a list, `concat` once |
| `s.apply(len)` | `s.str.len()` |

## Conditions

| Code | What it does |
|---|---|
| `np.where(condition, a, b)` | two choices |
| `np.select([c1, c2], [a, b], default=c)` | many choices; the first that holds wins |
| `s.clip(0, 100)` | squeezes between limits |
| `s.where(condition, other)` | replaces where the condition fails |

## Memory

| Code | What it does |
|---|---|
| `df.memory_usage(deep=True).sum()` | the real memory (text included) |
| `pd.to_numeric(s, downcast="integer")` | the smallest integer that fits |
| `s.astype("float32")` | half the memory, ~7 digits |
| `s.astype("category")` | text with few distinct values |
| `pd.read_csv(..., usecols=[...], dtype={...})` | choose while reading |

## Changing (pandas 3)

| Code | Result |
|---|---|
| `df.loc[condition, "a"] = 1` | `df` changes |
| `df[condition]["a"] = 1` | nothing; a `ChainedAssignmentError` warning |
| `part = df[condition]; part["a"] = 1` | only `part` changes |
| `df.assign(a=...)` | a new table; `df` stays the same |

## A chain

```python
result = (
    df.assign(total=lambda d: d["qty"] * d["price"])
      .query("total > @limit")
      .groupby("city")["total"].sum()
)
```
