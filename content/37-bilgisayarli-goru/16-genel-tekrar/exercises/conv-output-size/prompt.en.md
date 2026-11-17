`conv_output_size(size, kernel, stride, padding)` should return the side length
of the output when a convolution is applied to a square input: `(size + 2 ×
padding − kernel) / stride + 1`, rounded down.

**Expected output:**

```
32
16
24
```
