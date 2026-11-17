`decode_grid(output, S, size, threshold)` should take the probabilities
`[objectness, ox, oy, w, h, p0, p1, ...]` in each of the `S × S` cells and
turn the cells whose confidence (objectness × the largest probability) is
not below the threshold into `[x1, y1, x2, y2, class, confidence]` boxes
(confidence with 2 places; row by row, left to right).

**Expected output:**

```
[8.0, 0.0, 16.0, 8.0, 1, 0.81]
[0.0, 12.0, 4.0, 16.0, 0, 0.42]
[8.0, 8.0, 16.0, 16.0, 0, 0.4]
```
