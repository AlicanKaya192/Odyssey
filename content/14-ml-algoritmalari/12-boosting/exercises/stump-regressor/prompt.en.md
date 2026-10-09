Write the function `fit_stump_reg(x, y)`: a one-feature, one-question
regression tree. Sort by `x`; for each midpoint between different values
compute the two sides' sum of squared errors, choose the smallest (the smaller
threshold on a tie). Return the tuple `(threshold, left mean, right mean)`, all
three `round(..., 3)`.

**Expected output:**

```
(3.5, 1.033, 5.0)
```
