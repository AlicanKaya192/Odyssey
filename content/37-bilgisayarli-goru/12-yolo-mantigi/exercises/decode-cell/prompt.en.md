`decode_cell(row, col, values, S, size)` should turn a cell's `values` list
(`[objectness, ox, oy, w, h, p0, p1, ...]`) into a box:
`[x1, y1, x2, y2, class, confidence]`. The class is the position of the
largest probability, the confidence is objectness × that probability
(2 places).

**Expected output:**

```
[16.0, 4.0, 24.0, 20.0, 1, 0.8]
[0.0, 4.0, 4.0, 8.0, 2, 0.5]
```
