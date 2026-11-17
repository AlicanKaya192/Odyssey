`prepare(rows, labels)` turns the inputs into a tensor through NumPy, but the
types are wrong: the model wants `float32` inputs and `int64` labels. Fix the
function; it should return `[input type, label type, input shape]`.

**Expected output:**

```
['torch.float32', 'torch.int64', [3, 2]]
```
