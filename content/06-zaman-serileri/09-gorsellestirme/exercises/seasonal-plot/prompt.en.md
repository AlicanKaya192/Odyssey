Draw the seasonal plot that puts three years on top of each other: the
month on the horizontal axis, one line per year.

**What to do:**

1. Read the file. Build the table of means by month and year:
   `s.groupby([s.index.month, s.index.year]).mean().unstack()`.
2. Print the table's `shape` and its columns as a list.
3. Draw one line per year (`marker="o"`, labelled with the year), add a
   legend and save as `chart.png`.
4. Print each year's lowest and highest month as `year low high`, one per
   line (`idxmin()`, `idxmax()`).
5. Compute how much higher 2024 is than 2022 in each month and print the mean
   of those differences, rounded to one decimal.

**Expected output:**

```
(12, 3)
[2022, 2023, 2024]
2022 5 12
2023 6 12
2024 5 12
68.5
```

In all three years the peak is December and the low May or June: the lines
have the same shape, so the seasonality is stable. The distance between them is the
trend: 2024 sits on average 68 units above 2022 in every month.
