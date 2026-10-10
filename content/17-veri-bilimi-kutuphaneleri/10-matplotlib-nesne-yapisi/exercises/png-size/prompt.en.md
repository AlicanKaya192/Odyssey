`png_size(width, height, dpi)` should open a figure of size `figsize=(width,
height)`, draw a line in it and save it as `out.png` with **`dpi=dpi`** (do
not pass `bbox_inches`). Read the saved image with `matplotlib.image.imread`
and return `[width, height]` in pixels. Close the figure. Note:
`imread(...).shape` gives `(height, width, channels)`.

**Expected output:**

```
[400, 300]
[750, 300]
```
