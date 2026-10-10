`fitted_median(rows)` should build and fit a one-part `ColumnTransformer` that
fills `size` with the median (part name `"num"`) and return the learned
median, read from `named_transformers_["num"].statistics_`, as a
`float`.

**Expected output:**

```
95.0
```
