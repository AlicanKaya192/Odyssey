In the web traffic 14 March 2024 is a campaign day: 9593 visits. Compare
how the classical decomposition and robust STL react to that day.

**What to do:**

1. `classic = seasonal_decompose(visits, model="additive", period=7)`.
2. `robust = STL(visits, period=7, robust=True).fit()`.
3. Print the number of `NaN` values in the trend of the two methods on one
   line.
4. Print the trend on 14 March for the two methods, rounded to whole numbers,
   on one line (classical first).
5. Print the residual **one day before** the spike (13 March) for the two
   methods, rounded to whole numbers, on one line.
6. Print the residual of 14 March itself for the two methods, rounded to
   whole numbers, on one line.

**Expected output:**

```
6 0
4560 3737
-1206 -136
4487 5474
```

The classical trend bulges by 800 units on the day of the spike, because 9593
enters the average of seven days. The neighbours pay for it: 13 March gets a
large negative residual although nothing happened. With robust STL the trend
stays put, the neighbour's residual is small, and the whole spike sits in the
residual of its own day.
