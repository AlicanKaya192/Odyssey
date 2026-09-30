Read the coefficient table of the model fitted to the daily sales and
decide which terms really do any work.

`train` is ready in the starter code.

**What to do:**

1. Fit the `(1, 1, 1)(0, 1, 1, 7)` model.
2. For every coefficient except `sigma2` print its name, its value (two
   decimals) and its p-value (three decimals) as `name coefficient p`, one per
   line.
3. Print the names of the coefficients whose p-value is above 0.05 as a list.
4. Remove the term with the smallest coefficient (AR) and fit the
   `(0, 1, 1)(0, 1, 1, 7)` model. Print the AIC of the two models with one
   decimal on one line (the larger model first).
5. Print the residual standard deviation of the two models
   (`fit.resid.iloc[8:].std()`) with two decimals on one line.

**Expected output:**

```
ar.L1 0.11 0.001
ma.L1 -0.85 0.0
ma.S.L7 -0.86 0.0
[]
8258.7 8265.8
13.16 13.22
```

All three coefficients have a small p-value: the table shows none as
"unnecessary" and the list is empty. The AR coefficient is small (0.11) but
real; removing it makes the AIC 7 points worse. Yet the standard deviation of
the residual is almost the same, and in the rolling-origin table of the lesson
the two models gave the same error. **Being statistically significant does not
mean improving the forecast noticeably.** With a thousand observations very
small effects come out "significant" too; the out-of-sample error has the last
word.
