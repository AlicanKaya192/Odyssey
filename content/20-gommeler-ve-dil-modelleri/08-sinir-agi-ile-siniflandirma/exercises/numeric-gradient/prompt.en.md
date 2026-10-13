The loss of a small logistic model (`loss(w)`) is ready. `numeric_gradient(w,
eps)` should return, for each weight, the derivative `(loss(w + ε) − loss(w −
ε)) / 2ε` (nudging only that weight) with 4 places. Do not change `w`
itself.

**Expected output:**

```
[0.5692, -0.6805]
[0.3333, -0.5833]
```
