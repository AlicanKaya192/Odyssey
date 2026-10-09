Write the function `gradient_boost_1d(x, y, rounds, lr)`: the prediction
starts with the mean; `rounds` times fit a stump to the residuals with the
ready `fit_stump_reg` and add `lr ×` the stump's output to the prediction (the
left mean if `x ≤ threshold`, otherwise the right). Return the final training
MSE, `round(..., 4)`.

**Expected output:**

```
0 7.3325
1 3.13
5 0.0814
30 0.0048
```
