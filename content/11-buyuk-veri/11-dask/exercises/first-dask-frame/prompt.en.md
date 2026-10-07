Read four CSV files as a single dask table and see lazy evaluation.

**What to do:**

1. The starter code writes 200 000 orders as `orders-0.csv` …
   `orders-3.csv`.
2. `ddf = dd.read_csv("orders-*.csv")`; print the number of partitions.
3. `total = ddf["quantity"].sum()`; print the name of `total`'s type
   (`type(total).__name__`).
4. Print the result of `total.compute()`.
5. Print `len(ddf)`.

**Expected output:**

```
4
Scalar
443926
200000
```

Before `compute`, `total` is not a number but a recipe (`Scalar`).
