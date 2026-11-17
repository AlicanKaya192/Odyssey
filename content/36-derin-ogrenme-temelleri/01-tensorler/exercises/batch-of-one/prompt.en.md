Models always expect a **batch**: even a single grey image (height × width) is
given as `(1, 1, height, width)`. `batch_of_one(image)` should add two
dimensions in front of the two-dimensional tensor and return the new shape as a
list.

**Expected output:**

```
[1, 1, 2, 3]
```
