Some days are missing from `sales_messy.csv`. When you add up by week,
those gaps silently lower the total. Catch them.

**What to do:**

1. Read the file, sort it and add up the repeats
   (`sort_index().groupby(level=0).sum()`).
2. Compute the weekly total and the number of days per week in one table:
   `resample("W").agg(["sum", "count"])`.
3. Print the number of weeks with fewer than 7 observations.
4. Print the total and the number of days of the week ending 21 July 2024 on
   one line.
5. Make an estimate for that week **from the mean**: multiply the week's mean
   by 7, round to a whole number and print it.
6. Put the series on the calendar with `asfreq("D")`, add it up with
   `resample("W").sum(min_count=7)` and print the number of weeks that come
   out `NaN`.

**Expected output:**

```
6
1192 4
2086
6
```

That week's real total was 1892. The plain sum (1192) is far too low; the
estimate from the mean is too high, because the four remaining days run from
Thursday to Sunday, the high days of the week. `min_count` does neither: it
says "this week is incomplete".
