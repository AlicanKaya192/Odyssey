Do the first step of the classical decomposition by hand: the 7-day
**centred** moving average that cancels the weekly pattern.

The series is read in the starter code (`s`, daily, 1096 days).

**What to do:**

1. Compute `trend = s.rolling(7, center=True).mean()`.
2. Print the number of `NaN` values in the trend.
3. Print the first and the last date on which the trend is defined, on one
   line (`.date()`).
4. Print the trend value on those two dates, rounded to one decimal, on one
   line.
5. For comparison compute the trailing mean as well:
   `trailing = s.rolling(7).mean()`. Print the centred trend on 25 December
   2024 and the trailing mean on 28 December 2024 (one decimal) on one line.

**Expected output:**

```
6
2022-01-04 2024-12-28
230.1 393.3
386.1 386.1
```

The two numbers on the last line are the same: both are the mean of 22–28
December. The centred window writes that mean at the **middle** of the week
(the 25th), the trailing window at its **end** (the 28th). In a decomposition
the middle is the right place; the price is a three-day gap at each end.
