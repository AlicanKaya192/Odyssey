Write MASE and compare four forecasts on two series with different units
on the same scale.

**What to do:**

1. Write the function `mase(actual, forecast, train, m)` (all numpy arrays):
   the numerator is `np.mean(np.abs(actual - forecast))`, the denominator
   `np.mean(np.abs(train[m:] - train[:-m]))`.
2. **Daily sales** (`m = 7`; training up to 5 November 2024, the test being
   the next 28 days): print the MASE of the seasonal naive and the training
   mean forecasts, with two decimals, on one line.
3. **Monthly passengers** (`m = 12`; training up to the end of 2023, the test
   being 2024): print the MASE of seasonal naive (a copy of 2023) and of
   seasonal naive with growth (2023 × `total of 2023 / total of 2022`), with
   two decimals, on one line.
4. Print the denominator (the scale) of the two series, rounded to two
   decimals, on one line.

**Expected output:**

```
0.88 5.72
1.82 0.5
13.29 22.27
```

The four forecasts are now on the same ruler: the growth forecast for the
passengers (0.5) is best, seasonal naive on the sales (0.88) is below 1, plain
seasonal naive on the passengers (1.82) and the mean on the sales (5.72) are
above the bar. The two scales on the last line are very different; that is why
you could not compare the MAEs.
