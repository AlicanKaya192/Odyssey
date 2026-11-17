`encode(boxes, S, size, C)` should build the `(S, S, 5 + C)` target tensor
from the lesson out of `[x1, y1, x2, y2, class]` boxes and return it with
`.tolist()`: objectness, centre inside the cell, width and height relative to
the image, one-hot class.

**Expected output:**

```
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[1.0, 0.5, 0.25, 0.5, 0.25, 0.0, 1.0]
[1.0, 0.75, 0.0, 0.5, 0.5, 1.0, 0.0]
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```
