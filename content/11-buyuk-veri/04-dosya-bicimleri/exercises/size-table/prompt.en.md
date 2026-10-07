Write the same table in three formats and compare their sizes.

**What to do:**

1. The starter code prepares the typed `df` with 200 000 orders.
2. Write `df` as `orders.csv`, `orders.csv.gz` (both with `index=False`) and
   `orders.parquet`.
3. Loop over the three files; on each line print the file name and its size
   in MB (`os.path.getsize`, two decimals).
4. On the last line print the ratio of the CSV size to the Parquet size (one
   decimal).

**Expected output:**

```
orders.csv 11.99
orders.csv.gz 3.08
orders.parquet 4.29
2.8
```
