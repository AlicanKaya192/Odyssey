`missing_after_load(extra)` saves a small model and builds a longer model with
`extra` copies of `ReLU + Linear(3, 3)` added at the end. Load the saved
numbers into the longer model with `strict=False` and return the result's
`missing_keys` list.

**Expected output:**

```
['4.weight', '4.bias']
```
