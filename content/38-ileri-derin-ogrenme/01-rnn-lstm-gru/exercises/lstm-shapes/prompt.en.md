`lstm_shapes(input_size, hidden, layers, bidirectional, batch, steps)` should
build an `nn.LSTM` with `batch_first=True` and the given settings, pass an
input of zeros shaped `(batch, steps, input_size)` through it, and return the
shapes of `out`, `h` and `c` as lists.

**Expected output:**

```
[[2, 5, 3], [1, 2, 3], [1, 2, 3]]
[[2, 5, 6], [4, 2, 3], [4, 2, 3]]
```
