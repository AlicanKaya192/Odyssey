`bounding_box(img, threshold)` should return the box around the pixels whose
value is greater than `threshold` in a 2D picture (an `(H, W)` nested list)
as `[x1, y1, x2, y2]`: `x` is the column, `y` the row; `x2` and `y2` are
**not** inside the box (largest + 1). If there is no such pixel, an empty
list. The program tries the first three pictures of `make_shapes`.

**Expected output:**

```
triangle [5, 8, 11, 15]
square [4, 8, 10, 14]
triangle [3, 3, 11, 11]
```
