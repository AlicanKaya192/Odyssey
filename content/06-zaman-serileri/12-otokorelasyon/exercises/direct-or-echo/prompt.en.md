`temperature_daily.csv` holds six years of daily temperature (`date`,
`temp_c`). How long is the memory of the deviation from the seasonal normal,
and how much of it is direct?

**What to do:**

1. Compute the seasonal normal: the six-year mean for each calendar day
   (`t.groupby(t.index.dayofyear).transform("mean")`). The deviation:
   `anomaly = t - normal`.
2. Print the ACF of the anomaly for the first 5 lags, rounded to two
   decimals, as a list (lag 0 excluded).
3. Print the PACF of the anomaly for the same 5 lags.
4. If "only yesterday mattered", the ACF would decay as `r, r², r³, ...`.
   Take `r` as the ACF at lag 1 and print its first 5 powers, rounded to two
   decimals, as a list.
5. Print the ACF of the raw temperature (`t`) at lags 1 and 365, rounded to
   two decimals, on one line.

**Expected output:**

```
[0.72, 0.51, 0.38, 0.28, 0.19]
[0.72, -0.03, 0.06, -0.02, -0.03]
[0.72, 0.52, 0.38, 0.27, 0.2]
0.97 0.74
```

The ACF shows a long tail, but the PACF has only lag 1: two days ago does not
affect today directly. The third line confirms it: the powers of `r` are very
close to the actual ACF. In the raw temperature lag 365 is still very high:
that is not memory, it is the yearly season.
