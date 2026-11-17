`hook_shape(index, size)` should attach a forward hook to the model's layer
number `index`, run it once with a zero input of `(1, 1, size, size)` and
take the captured output's shape, then remove the hook and run the model
once more. Return `[captured shape, number of captured outputs]` (the removed
hook must not add anything on the second run).

**Expected output:**

```
[[1, 8, 8, 8], 1]
[[1, 16, 6, 6], 1]
```
