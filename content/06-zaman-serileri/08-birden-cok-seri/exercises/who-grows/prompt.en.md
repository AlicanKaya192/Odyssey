In raw sales A is always ahead. To compare growth, start the series from
the same point.

**What to do:**

1. Read `stores.csv` and turn it into the wide shape.
2. Compute the monthly means: `wide.resample("ME").mean()`.
3. Build the index that takes May 2024 as 100:
   `monthly / monthly.loc["2024-05-31"] * 100`.
4. Print the index values of December 2024 as a dict rounded to one decimal.
5. From quarterly totals compute each shop's share (percent) and print the
   shares of the last quarter as a dict rounded to one decimal.
6. Print by how many **points** A's share changed from the first quarter to
   the last, rounded to one decimal.

**Expected output:**

```
{'A': 120.3, 'B': 116.8, 'C': 114.1, 'D': 182.2}
{'A': 35.7, 'B': 19.7, 'C': 22.9, 'D': 21.7}
-8.1
```

The smallest shop is the fastest growing. A's share fell, but its own sales
grew 20 percent: the share shrank because a new shop entered the
denominator.
