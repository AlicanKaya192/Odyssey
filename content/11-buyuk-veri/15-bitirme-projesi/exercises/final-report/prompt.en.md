Produce a short report for the manager from the Parquet file: exact numbers
from DuckDB, a quick estimate from a sample.

**What to do:**

1. `orders.parquet` is ready (300 000 orders, with a `month` column).
2. DuckDB: find the top three cities by revenue and each one's share of the
   total revenue (percent, one decimal); city and share on each line.
3. DuckDB: print the month with the highest mean revenue per order and that
   mean (two decimals).
4. A quick estimate: read the file with pandas and take a sample with
   `sample(frac=0.01, random_state=3)`; work out the mean revenue per order
   from the sample and from the whole. Print both (two decimals) and the
   error (percent, one decimal) on one line.

**Expected output:**

```
Istanbul 34.0
Ankara 15.9
Izmir 13.2
2024-05 1665.57
1627.57 1642.77 0.9
```
