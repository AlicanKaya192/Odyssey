Compare the plain difference with the seasonal difference on the daily
sales, then show that differencing loses no information.

**What to do:**

1. Print the standard deviation of the series, of `s.diff()` and of
   `s.diff(7)`, rounded to one decimal, on one line.
2. Print the number of `NaN` values in the same three series on one line.
3. Is the weekly pattern gone? For `s.diff()` and `s.diff(7)` take the mean by
   day of the week and print, for each, the difference between the highest and
   the lowest day, rounded to one decimal, on one line.
4. Undo the plain difference: `back = s.diff().cumsum() + s.iloc[0]`. Is it
   the same as the series apart from the first row? Print the result of
   `(back.iloc[1:] - s.iloc[1:]).abs().max() < 1e-9`.
5. Undo the seasonal difference by one step: compute the value of the last day
   of the series as the last value of `s.diff(7)` plus the sales 7 days
   earlier, and print it on one line together with the actual last value.

**Expected output:**

```
58.9 46.1 17.1
0 1 7
136.7 0.4
True
347 347
```

With the plain difference there is still a large gap between the days of the
week: the pattern is in place. With `diff(7)` it is almost zero. And both
differences can be undone: the model forecasts the difference, and you turn it
into a level.
