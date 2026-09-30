The same 28-day mean, placed two ways: trailing and centred. When does
each one show the year-end peak?

**What to do:**

1. Read the file. Compute two series: `s.rolling(28).mean()` and
   `s.rolling(28, center=True).mean()`.
2. In the stretch from 15 November 2023 to 15 February 2024, print the date
   (`"%Y-%m-%d"`) on which each is highest, one per line: the centred one
   first, then the trailing one.
3. Print the difference between the two dates in days.
4. Print the values of the two peaks, rounded to one decimal, on one line.
5. Print, on one line, how many `NaN` values each has in the **last 14 days**
   of the series: the centred one first, then the trailing one.

**Expected output:**

```
2023-12-19
2024-01-01
13
330.9 330.9
13 0
```

The height of the peak is the same, its date 13 days apart: the trailing
mean is the same curve shifted to the right. The last line shows the price of
the centred window: there are no values for the most recent days of the
series, because what comes "after" those days has not happened yet.
