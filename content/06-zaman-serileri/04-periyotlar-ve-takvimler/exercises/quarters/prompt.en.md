Add sales up into quarters and look at how the year closed.

**What to do:**

1. Read the file and compute the quarterly totals (`to_period("Q")`).
2. Print the four quarters of 2024 as `quarter total`, one per line.
3. Print by what percentage the fourth quarter of 2024 is above the first,
   rounded to one decimal.
4. Print the percentage change of the last quarter of 2024 against the last
   quarter of 2023, rounded to one decimal.

**Expected output:**

```
2024Q1 26513
2024Q2 24146
2024Q3 26025
2024Q4 30927
16.6
12.0
```

The rise in the third line is seasonality (the end of the year is always
high); the rise in the fourth line is trend (the same quarter, a year later).
The way to tell them apart is to compare **the same period**.
