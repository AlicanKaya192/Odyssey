Write the function `prf(y, pred)`: it returns the tuple
`(precision, recall, f1)`, all three `round(..., 3)`. If a denominator is 0,
that measure is 0.0 (precision is 0 if there is no positive prediction, F1 is 0
if precision + recall is 0).

**Expected output:**

```
(0.75, 0.75, 0.75)
(0.0, 0.0, 0.0)
```
