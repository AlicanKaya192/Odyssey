A 365-day window suppresses both the weekly and the yearly pattern; what
is left is the trend.

**What to do:**

1. Read the file and compute the 365-day moving average.
2. Print the number of `NaN` values at the start.
3. Print the values on 31 December 2022, 2023 and 2024, rounded to one
   decimal, on one line.
4. Print the means of the same three years (`s.resample("YE").mean()`) as a
   list rounded to one decimal.
5. Find how much the trend rose in a year: subtract the value on 31 December
   2023 from that on 31 December 2024 and round to one decimal.

**Expected output:**

```
364
225.5 260.4 294.1
[225.5, 260.4, 294.0]
33.7
```

The moving average at the end of each year is almost the same as that year's
mean (2024 is a leap year, so the window covers 365 of its 366 days). The
price is in the first line: nearly a year of data goes into computing the
trend.
