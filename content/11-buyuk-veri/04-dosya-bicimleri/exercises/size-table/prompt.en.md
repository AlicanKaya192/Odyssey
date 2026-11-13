Write the same table in three formats and compare their sizes.

**What to do:**

1. The starter code prepares the typed `df` with 200 000 orders.
2. Write `df` as `orders.csv`, `orders.csv.gz` (both with `index=False,
   lineterminator="\n"`) and `orders.parquet`. Giving the line ending
   makes the sizes the same on every computer.
3. Loop over `orders.csv` and `orders.parquet`; on each line print the
   file name and its size in MB (`os.path.getsize`, two decimals).
4. On the next line print how many times smaller gzip makes the CSV (the CSV
   size / the gzipped size), rounded to a whole number. gzip's output can
   differ by a few KB with Python's compression library; the whole number is
   the same on every computer.
5. On the last line print the ratio of the CSV size to the Parquet size (one
   decimal).

**Expected output:**

```
orders.csv 11.79
orders.parquet 4.29
4
2.7
```
