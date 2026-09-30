`two_processes.csv` comes from Section 12: `x` was produced by an AR(1)
process and `y` by an MA(1), both with a coefficient of 0.7. Pretend you do
not know that and ask the model.

**What to do:**

1. Read the file as a table `w` with a date index.
2. For each series fit two models: `order=(1, 0, 0)` and `order=(0, 0, 1)`.
   Print their AICs with one decimal as `series AR_aic MA_aic`, one per line.
3. For each series print the coefficient (`ar.L1` or `ma.L1`) of the model
   with the smaller AIC, with two decimals, as `series kind coefficient` (the
   kind being `AR` or `MA`).
4. Fit a model larger than needed to series `x`: `order=(2, 0, 0)`. Print the
   second AR coefficient (`ar.L2`) and its p-value (`fit.pvalues["ar.L2"]`)
   with two decimals on one line.
5. Print the AIC of that model together with the AIC of AR(1), with one
   decimal, on one line (AR(1) first).

**Expected output:**

```
x 1622.9 1744.9
y 1722.5 1625.2
x AR 0.69
y MA 0.7
-0.02 0.64
1622.9 1624.7
```

The AIC picks the right kind for both series by more than a hundred points and
finds a coefficient around 0.7. The extra second AR term is close to zero, its
p-value is large and it makes the AIC **worse**: all three signs of an
unnecessary term at once.
