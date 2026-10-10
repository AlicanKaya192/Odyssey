`l1_columns(c)` should build a `SelectFromModel` with
`LogisticRegression(penalty="l1", C=c, solver="liblinear")`, `fit` it on the
data in the starter code and return the positions of the selected columns as
a list. The smaller `C`, the fewer columns should remain.

**Expected output:**

```
[0, 1, 2, 3]
[0, 2]
```
