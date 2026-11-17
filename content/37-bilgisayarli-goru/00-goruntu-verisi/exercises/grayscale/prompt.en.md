`grayscale(rgb)` should turn a colour picture in `(3, H, W)` order into a grey
one: each pixel is `0.299 * R + 0.587 * G + 0.114 * B`. Return the result as
an `(H, W)` nested list with values rounded to 3 places.

**Expected output:**

```
[[0.299, 0.587]]
[[0.5]]
```
