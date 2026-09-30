Suppose you do not know the length of the season of the hourly
electricity load. Ask the ACF.

**What to do:**

1. Compute `values = acf(load, nlags=200)`.
2. Print the lag of the highest ACF among lags 2–30 and its value (two
   decimals) on one line.
3. Print the lag and value of the **lowest** ACF in the same range.
4. Print the lag and value of the highest ACF among lags 100–200.
5. Print the ACF at the multiples of 24 (24, 48, 72, ..., 168), rounded to two
   decimals, as a list.

**Expected output:**

```
24 0.88
13 -0.47
168 0.87
[0.88, 0.77, 0.77, 0.76, 0.74, 0.81, 0.87]
```

The first peak is at lag 24: the daily period. Half a day later (12–13 hours)
goes the opposite way: day and night. The peak in the distant range is at 168: the
weekly period. On the last line the ACF at the multiples of 24 first falls and
then rises again at 168: seven days later resembles today more than three days
later does.
