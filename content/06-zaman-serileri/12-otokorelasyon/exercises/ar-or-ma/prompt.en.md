`two_processes.csv` holds two series of 600 days (`date`, `x`, `y`). One
was produced by an AR(1) process, the other by an MA(1). Find out which is
which from their correlograms.

**What to do:**

1. Read the file as a table `w` with a date index.
2. For `x` print the ACF and the PACF at the first 4 lags, rounded to two
   decimals, as lists on two separate lines.
3. Print the same for `y`.
4. Write a function `kind(series)`: it takes the band as
   `1.96 / np.sqrt(len(series))`. If **the ACF at lag 2** is inside the band
   (the ACF cut off after lag 1) it returns `"MA"`, otherwise `"AR"`.
5. Print the results of `kind(w["x"])` and `kind(w["y"])` on one line.

**Expected output:**

```
[0.69, 0.46, 0.32, 0.23]
[0.69, -0.02, 0.01, 0.03]
[0.46, -0.04, -0.04, -0.03]
[0.46, -0.31, 0.17, -0.14]
AR MA
```

For `x` the ACF fades step by step and the PACF is zero after lag 1: AR. For
`y` it is the other way round: the ACF is zero after lag 1 and the PACF decays
changing sign: MA. Both were produced with a coefficient of 0.7; the same
number gives a very different memory in the two processes.
