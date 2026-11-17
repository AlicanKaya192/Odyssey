`output_size(h, k, stride, padding)` should compute a convolution layer's
output size with the formula `(h + 2 * padding - k) // stride + 1`.

**Expected output:**

```
16 3 1 0 14
16 3 1 1 16
16 3 2 1 8
32 5 2 0 14
```
