The `score` column is text and contains two fake values: `"abc"` and
`"-1"`. Both mean "unknown" but they look different.

**What you need to do:**

1. Convert the `score` column to numeric. Values that cannot be converted
   should come out empty **rather than raising**.
2. Turn the value `-1` into a real missing value (`np.nan`).
3. Print the column's values as a list.
4. Print the column's type.
5. Print how many values are missing.

**Expected output:**

```
[82.0, 74.0, 91.0, 82.0, nan, 88.0, nan]
float64
2
```

**Two important points:**

- Had you tried `astype(float)`, `"abc"` would have made the **whole
  program** fail. `pd.to_numeric(..., errors="coerce")` confines the problem
  to a single cell.
- `-1` converts to a number but is **not a real score**. Leave it as it is
  and it gets mixed into the average and ruins the result. Fake gaps like
  `-1`, `999` and `"N/A"` are very common in real data.

The result is `float64` because the integer type cannot hold `NaN`.
