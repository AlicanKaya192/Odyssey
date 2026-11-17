`find_pattern(img, pattern)` should use the pattern as a kernel, find the
strongest response in the picture with `F.conv2d` (no padding) and return
its `[row, column]` in the output (where the pattern's top-left corner sits
in the picture). `argmax` gives a flat index; turn it into row and
column.

**Expected output:**

```
[2, 3]
[3, 3]
```
