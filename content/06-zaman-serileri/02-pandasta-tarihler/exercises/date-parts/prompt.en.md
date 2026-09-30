In Section 00 the days of the week came in a ready-made column. Now
build it from the date yourself and measure the shop's weekly pattern.

**What to do:**

1. Read `store_sales.csv` with `parse_dates=["date"]`.
2. Compute the mean sales by day name (`dt.day_name()`) and sort from largest
   to smallest. Print the **first three** days as `name mean` (one decimal),
   one per line.
3. Print the weekend's (`dt.dayofweek >= 5`) percentage share of total sales,
   rounded to one decimal.
4. Print the total sales of March 2024 (`dt.year` and `dt.month`).

**Expected output:**

```
Saturday 336.1
Sunday 296.9
Friday 278.9
34.9
8919
```

The weekend is 2/7 of the calendar, about 28.6%. Its share of sales being
higher than that is the measure of the weekly seasonality.
