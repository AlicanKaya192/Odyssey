`mask_boxes(mask)` should return, for each class (1 and above) in the mask,
the box holding all pixels of that class as `[x1, y1, x2, y2, class]`, in
class order. `x2` and `y2` are not included (largest + 1). Skip a class not
in the mask.

**Expected output:**

```
[0, 3, 1, 4, 1]
[1, 1, 3, 3, 2]
[4, 2, 5, 4, 3]
```
