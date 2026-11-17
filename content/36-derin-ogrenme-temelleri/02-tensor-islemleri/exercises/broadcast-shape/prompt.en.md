`result_shape(shape_a, shape_b)` should add two tensors of zeros (`torch.zeros`)
of the given shapes and return the result's shape as a list. If the shapes cannot
be broadcast (`RuntimeError`), it should return `"error"`.

**Expected output:**

```
[3, 2]
[3, 4]
error
```
