`gradients(w_value, x, b_value, target)` should build `w` and `b` as tensors
that want gradients, compute the loss as `(w·x + b − target)²` and return `[w's
gradient, b's gradient]`.

**Expected output:**

```
[12.0, 4.0]
[2.0, -2.0]
```
