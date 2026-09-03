You are going to build three measures without calling a library. Writing
the formula out once by hand is what lets you know what those numbers mean
in every section that follows.

You have the actual prices of eight houses and a model's predictions.

**What you need to do:**

1. Compute the **residual** for each record (`actual - predicted`) and print
   the list as it is.
2. Compute **MAE**: the mean of the residuals' absolute values. Print it to
   two decimals.
3. Compute **MSE**: the mean of the residuals' squares.
4. Compute **RMSE**: the square root of MSE.
5. Print MSE and RMSE **side by side** (two decimals).

**Expected output:**

```
[12, -7, -15, 15, -15, 30, -8, 10]
14.0
241.5 15.54
```

**Look at the signs on the first line.** A positive residual means the model
predicted **too low**; a negative one that it predicted too high. Had you
summed them, +12 and -15 would cancel and the model would look better than
it is. Both the absolute value and the square exist to stop exactly that.

**MAE 14.0, RMSE 15.54.** RMSE is larger — and it always will be larger or
equal. The gap comes from the `30` in the list: squaring punishes a large
error disproportionately. The wider the gap, the surer you can be that a few
large errors are in there.

**That MSE came out 241.5 is worth noticing:** its unit is the target's unit
squared, so the number says nothing on its own. That is why the square root
is taken.
