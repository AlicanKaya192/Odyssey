Split the daily sales into training and test and build the index of the
forecast.

In the starter code the series is ready as `s`, cut at 3 December 2024.

**What to do:**

1. Make the last 28 days the test and what comes before the training:
   `train = s.iloc[:-28]`, `test = s.iloc[-28:]`.
2. Print the lengths of training and test on one line.
3. Print the last date of the training and the first date of the test on one
   line (`.date()`).
4. Take the horizon `h = len(test)` and build the index of the future dates:
   `pd.date_range(train.index[-1] + pd.Timedelta(days=1), periods=h, freq="D")`.
5. Print the first and the last date of that index on one line.
6. Is the index you built the same as the index of the test? Print the result
   of `future.equals(test.index)`.
7. Print the mean of training and test, rounded to one decimal, on one line.

**Expected output:**

```
1040 28
2024-11-05 2024-11-06
2024-11-06 2024-12-03
True
255.1 331.1
```

The test starts the day after the training ends, and there is no overlap
between them. The mean of the test is clearly above that of the training: the
series is growing and we are nearing the end of the year. That is why using
the mean of the past as a forecast will be a bad idea.
