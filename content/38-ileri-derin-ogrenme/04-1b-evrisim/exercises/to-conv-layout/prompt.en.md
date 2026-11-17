`to_conv_layout(batch)` should turn a batch in LSTM layout `(B, T, D)` into
the `(B, D, T)` layout `Conv1d` wants, and return it as a list.

**Expected output:**

```
[[[1, 4], [2, 5], [3, 6]]]
```
