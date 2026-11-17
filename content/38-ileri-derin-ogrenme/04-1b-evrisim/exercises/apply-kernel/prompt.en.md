`apply_kernel(signal, kernel)` should build an `nn.Conv1d(1, 1, len(kernel))`
without a bias, set its weight to `kernel`, pass the signal through it as
`(1, 1, T)` and return the output as a flat list.

**Expected output:**

```
[0.0, 1.0, 2.0, 0.0, -2.0, -1.0]
[6.0, 9.0]
```
