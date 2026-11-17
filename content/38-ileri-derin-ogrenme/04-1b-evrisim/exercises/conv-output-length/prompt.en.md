`conv_output_length(length, kernel, padding, stride)` should compute the
output length of an `nn.Conv1d` with the formula `(length + 2·padding −
kernel) // stride + 1`.

**Expected output:**

```
60
64
30
```
