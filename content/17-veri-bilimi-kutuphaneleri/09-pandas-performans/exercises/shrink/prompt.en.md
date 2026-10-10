`shrink(qtys, prices)` should build a two-column table (`qty`, `price`). It
should shrink `qty` with `pd.to_numeric(..., downcast="unsigned")` and `price`
with `astype("float32")`. Return:

- `"dtypes"`: the new types as a list of text (`dtypes.astype(str).tolist()`)
- `"smaller"`: whether the new table uses less memory than the old (`bool`)

Measure memory with `memory_usage(deep=True).sum()`.

**Expected output:**

```
['uint8', 'float32']
True
```
