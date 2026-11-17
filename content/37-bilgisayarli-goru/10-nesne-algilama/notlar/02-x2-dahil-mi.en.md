Is a box's bottom-right corner the last pixel **itself**, or **one past** it?
Both conventions exist and mixing them silently changes the area and the IoU.
`make_scenes` uses the second: `x2` is one past the last column. Let us check
it with the mask:

```python
import numpy as np
from dl_data import make_scenes

images, boxes, masks = make_scenes(100, size=32, seed=7)
x1, y1, x2, y2, label = boxes[0][0]
ys, xs = np.nonzero(masks[0] == label + 1)
print(xs.min(), xs.max(), x1, x2)
print(ys.min(), ys.max(), y1, y2)
print((x2 - x1) * (y2 - y1))
print((xs.max() - xs.min()) * (ys.max() - ys.min()))
```

```text
17 25 17 26
7 15 7 16
81
64
```

- The shape's rightmost pixel is in column 25, while `x2` is 26: one past.
  The same holds for `y2`.
- In this convention the width is simply `x2 − x1` (9 pixels) and the area 81.
- If someone writes the same box "last pixel included" (`x2 = 25`) and still
  computes the area as `x2 − x1`, they get 64: one pixel lost on each side.
  On small objects this difference changes the IoU noticeably.

torchvision's box functions assume continuous coordinates: `x2 − x1` is the
width. Check your own dataset's convention once, then keep it the same in all
your code.
