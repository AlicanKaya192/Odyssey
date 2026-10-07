Work out three different results with a single `dask.compute` call.

**What to do:**

1. The starter code writes the four CSV files; read them with `dd.read_csv`.
2. Build three recipes:
   - the mean `unit_price`,
   - the number of orders with `quantity >= 4` (`shape[0]`),
   - the number of different cities (`nunique()`).
3. Work out all three with a single `dask.compute(...)`.
4. Print the mean rounded to two decimals and the other two as they are, on
   separate lines.

**Expected output:**

```
739.31
44225
8
```
