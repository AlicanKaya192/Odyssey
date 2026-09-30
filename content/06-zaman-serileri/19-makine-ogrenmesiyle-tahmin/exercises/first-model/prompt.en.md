Fit a linear regression on the feature table and compare it with the
baselines. In the starter code `table`, `columns`, `train` (up to the end of
2023) and `test` (2024) are ready.

**What to do:**

1. Fit `LinearRegression().fit(train[columns], train["y"])` and forecast 2024.
2. Print the test error (MAE) of three methods with two decimals on one line:
   naive (`test["lag1"]`), seasonal naive (`test["lag7"]`), the linear model.
3. Print the training and test error of the linear model with two decimals on
   one line.
4. Print the skill of the model over seasonal naive
   (`1 - MAE / MAE_snaive`) with two decimals.
5. Print the coefficients as `name coefficient`, with two decimals, sorted by
   absolute value from largest to smallest.

**Expected output:**

```
41.1 13.87 11.51
10.89 11.51
0.17
dow 2.07
month 1.4
lag14 0.43
lag7 0.42
mean7 0.14
lag1 0.05
mean28 -0.03
lag2 -0.02
```

The linear model beats seasonal naive, and its training and test errors are
close: no memorising. Among the lags the largest weights are on `lag14` and
`lag7`: the model leans on **the same weekday** of past weeks, and `lag1` is
almost zero. The coefficients of `dow` and `month` look large but are in other
units (per day or month number); coefficients can only be compared between
features on the same scale. Giving `dow` as a single number is not a good
encoding for a linear model either (see the notes).
