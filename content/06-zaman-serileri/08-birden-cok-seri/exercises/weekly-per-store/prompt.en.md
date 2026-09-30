Compute each shop's weekly total in the long shape.

**What to do:**

1. Read `stores.csv`.
2. Compute the total per shop and week:
   `long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()`.
3. Print the number of rows in the result.
4. Print shop A's first two weeks as a list
   (`weekly.loc["A"].head(2).tolist()`).
5. For each shop print the highest weekly total and that week's label
   (`"%Y-%m-%d"`) as `shop date total`, one per line.

**Expected output:**

```
195
[2296, 2297]
A 2024-12-29 2590
B 2024-01-14 1393
C 2024-01-07 1666
D 2024-12-22 1618
```

All four shops peak around the turn of the year: they share a common yearly
seasonality. But the growing shops A and D peak in December, while B and C,
which are not growing, peak in January: the trend decides which end of the
season comes out higher. The number of rows is below 4 × 53, because D opened
in the middle of the year.
