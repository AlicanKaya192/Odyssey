`converges(lr)` should train the linear model on the ready data for `steps`
rounds of gradient descent and return `True` if the last loss is smaller than the
first, otherwise (if it diverged) `False`. The results of three learning rates are
printed.

**Expected output:**

```
0.001 True
0.05 True
0.5 False
```
