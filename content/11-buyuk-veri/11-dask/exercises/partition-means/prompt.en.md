Show with dask why the mean of means is wrong when partitions differ in
size.

**What to do:**

1. Split the table `make_orders(120_000)` into three files: `part-0.csv`
   (the first 50 000), `part-1.csv` (the next 50 000), `part-2.csv` (the last
   20 000); `index=False`.
2. `ddf = dd.read_csv("part-*.csv")`; get each partition's number of rows
   with `ddf.map_partitions(len).compute()` and print it as a list.
3. Get each partition's mean `unit_price` with
   `ddf.map_partitions(lambda p: p["unit_price"].mean()).compute()`; print the
   mean of these, rounded to four decimals.
4. Print dask's own mean (`ddf["unit_price"].mean().compute()`), rounded to
   four decimals.
5. Print whether the two values are equal.

**Expected output:**

```
[50000, 50000, 20000]
740.419
738.3869
False
```

dask's `mean` accumulates the total and the count separately (Section 3); the
mean of the partition means gives too much weight to the small partition.
