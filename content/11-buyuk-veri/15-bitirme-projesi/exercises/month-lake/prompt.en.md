Split the orders into month folders and query only one month with DuckDB.

**What to do:**

1. `orders` and the `month` column are ready. For every month write the file
   `lake/month=<month>/part-0.parquet` (the `month` column should not go into
   the file).
2. Print the number of folders.
3. With DuckDB find the three categories with the highest revenue in June
   (`'2024-06'`) in the lake, rounding the revenue to two decimals; print the
   category and the revenue on each line.
4. Run `EXPLAIN ANALYZE SELECT count(*) ...` with the same filter and print
   the information about the files scanned from the plan text:
   `re.search(r"Scanning Files: \d+/\d+", plan).group()`.

**Expected output:**

```
12
electronics 19835690.29
clothing 6965783.83
home 5271617.01
Scanning Files: 1/12
```
