Is there a trend? The simplest way is to look at each year's average:
a yearly average smooths out the weekly and monthly swings and leaves the
long-term direction.

The dates are still text. You will learn to turn them into a date type in
Section 02; for now use one more advantage of ISO 8601: **the year is always
the first four characters.**

```python
table["date"].str[:4]    # "2022-01-01" -> "2022"
```

**What to do:**

1. Read `store_sales.csv`.
2. Create a new column called `year`: the first four characters of the date.
3. Group by year and take the mean of sales, rounded to one decimal. Print
   each year on its own line as `year mean`.
4. Print, rounded to one decimal, by what percentage the last year's mean
   grew compared with the first: `(last / first - 1) * 100`.

**Expected output:**

```
2022 225.5
2023 260.4
2024 294.0
30.4
```

About a third of growth in two years: a clear upward trend.
