`mha_params(dim, heads)` should build an `nn.MultiheadAttention(dim, heads)`
and return its total parameter count. Look at whether the head count changes
the result.

**Expected output:**

```
288
288
16640
```
