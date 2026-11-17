`golden_ok(expected, actual, atol)` should return whether the loaded model's
output (`actual`) and the golden output in the delivery package (`expected`)
are the same within `atol` (`torch.allclose`).

**Expected output:**

```
True
False
```
