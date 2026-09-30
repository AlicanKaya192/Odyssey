Fit two models to the café sales: one with the past of the series only,
the other with three external variables. Read the coefficients.

In the starter code `train` (up to 31 October 2024) and `columns` are ready.

**What to do:**

1. The model without external variables:
   `ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()`.
2. The model with external variables: the same, with `exog=train[columns]`.
3. Print the AIC of the two models with one decimal on one line (the one
   without first).
4. Print the coefficient of the three external variables as `name coefficient`
   with one decimal, one per line.
5. Print the 95% confidence interval of the three coefficients: from the
   `fit.conf_int()` table the lower and upper bound for each variable (one
   decimal), as `name lower upper`.
6. Print the residual standard deviation of the two models
   (`resid.iloc[8:].std()`) with one decimal on one line.

**Expected output:**

```
9464.3 7568.8
promo 49.3
holiday -75.2
temp_c 5.5
promo 46.1 52.5
holiday -78.0 -72.5
temp_c 5.3 5.7
24.0 9.4
```

The coefficients read directly: a campaign day is +49, a holiday −75, each
degree +5.5. The confidence intervals are narrow and far from zero: all three
effects are clear. The standard deviation of the residual falls from 24 to 9: the
model now explains most of what it used to count as "surprise".
