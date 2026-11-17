`state_summary(sizes)` should return a `[name, number of elements]` list for
every key in the state_dict of the model built with `build(sizes)`. The number
of elements is `tensor.numel()`.

**Expected output:**

```
['0.weight', 32]
['0.bias', 8]
['2.weight', 24]
['2.bias', 3]
```
