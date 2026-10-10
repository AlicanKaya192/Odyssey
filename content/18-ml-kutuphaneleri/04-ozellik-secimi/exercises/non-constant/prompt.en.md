`non_constant(rows)` should find the columns that never change with
`VarianceThreshold(threshold=0)` and return the positions of the **remaining**
columns (`get_support(indices=True)`) as a list.

**Expected output:**

```
[1]
```
