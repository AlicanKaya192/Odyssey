`info(rows)` should build a tensor from a Python list and return `[shape list,
type text]`. Write the shape with `list(t.shape)` and the type with
`str(t.dtype)`.

**Expected output:**

```
[[2, 3], 'torch.int64']
[[2], 'torch.float32']
```
