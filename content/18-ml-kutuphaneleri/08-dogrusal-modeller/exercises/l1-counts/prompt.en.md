`l1_counts(c)` should train an L1-penalised logistic regression on the scaled wine
data (`Xs`) (`l1_ratio=1`, `solver="saga"`, `C=c`, `max_iter=5000`) and return
each class's number of non-zero coefficients as a list. `penalty=` is
deprecated; do not use it. The starter code uses the default (L2) penalty.

**Expected output:**

```
[3, 8, 4]
[4, 4, 4]
```
