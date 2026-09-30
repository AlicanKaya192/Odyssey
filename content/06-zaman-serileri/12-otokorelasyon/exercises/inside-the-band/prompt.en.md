Compare the correlogram of the price series and of its daily change with
the confidence band.

**What to do:**

1. Write a function `outside(x, nlags=20)`: it computes
   `acf(x, nlags=nlags)`, takes the band as `1.96 / np.sqrt(len(x))` and
   returns, lag 0 excluded, the **lag numbers** whose absolute value is beyond
   the band, as a list.
2. Print the band for the daily change (`k.diff().dropna()`), rounded to
   three decimals.
3. Print the lags beyond the band for the daily change.
4. Print the **number** of lags beyond the band for the price itself.
5. Print the ACF of the price at lags 1, 10 and 20, rounded to two decimals,
   as a list.

**Expected output:**

```
0.07
[2]
20
[0.99, 0.87, 0.76]
```

For the daily change only one of 20 lags is beyond the band; with a 95% band
that is what chance alone would give. For the price itself all 20 are outside
and they decay very slowly: that is not memory, it is a trend.
