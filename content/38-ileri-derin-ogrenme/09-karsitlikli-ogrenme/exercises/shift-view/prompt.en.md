`shift_view(image, dx, dy, flip)` should shift a two-dimensional image (an
`(H, W)` list) with `torch.roll` by `dy` along the rows and `dx` along the
columns; if `flip` is true, then flip it horizontally (`flip(-1)`). Return a
list.

**Expected output:**

```
[[3.0, 1.0, 2.0], [6.0, 4.0, 5.0]]
[[6.0, 5.0, 4.0], [3.0, 2.0, 1.0]]
```
