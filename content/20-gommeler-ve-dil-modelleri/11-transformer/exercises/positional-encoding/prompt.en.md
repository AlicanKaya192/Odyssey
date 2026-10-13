`positional_encoding(n, d)` should build the lesson's sine encoding: for each
`pos`, at steps `i = 0, 2, 4, ...`, `angle = pos / 10000 ** (i / d)`; add
`sin(angle)` then `cos(angle)` to the row. 3 places.

**Expected output:**

```
[0.0, 1.0, 0.0, 1.0]
[0.841, 0.54, 0.01, 1.0]
[0.909, -0.416, 0.02, 1.0]
```
