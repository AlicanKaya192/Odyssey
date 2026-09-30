Run the same 28-day experiment from two different origins and look at the
**direction** of the error of seasonal naive.

In the starter code the function `snaive(train, h)` is ready: it returns a
list repeating the last week for `h` days.

**What to do:**

1. Write a function `evaluate(cut)`: the data up to the date `cut` is the
   training, the next 28 days the test. Build the seasonal naive forecast and
   return three things as a tuple: the mean absolute error (two decimals), the
   bias (two decimals), and the number of days on which the forecast was
   **too low** (`error > 0`).
2. Print the results of `evaluate("2024-11-05")` and `evaluate("2024-12-03")`,
   one per line.
3. For the second experiment (3 December) print the mean of the error by
   week: split the 28 days of errors into four pieces of 7 and print the mean
   of each piece, rounded to one decimal, as a list.

**Expected output:**

```
(11.64, 6.79, 20)
(40.25, 40.25, 28)
[19.4, 35.0, 43.9, 62.7]
```

In the November experiment the bias is about half the MAE: the errors go both
ways. In the December experiment the MAE and the bias are the same: the
forecast is low on all 28 days. The last line shows why: the error grows from
week to week. While the year-end climb goes on, the forecast stays at the
level of late November.
