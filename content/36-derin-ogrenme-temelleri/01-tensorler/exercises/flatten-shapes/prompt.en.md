`flatten_shapes(n, size)` makes the images with `make_shapes(n, size=size)`.
Turn them into a tensor and flatten them keeping the first dimension; return the
flat tensor's shape and how many images are circles (label 0) in one list:
`[rows, columns, circle count]`.

**Expected output:**

```
[50, 256, 15]
[20, 64, 7]
```
