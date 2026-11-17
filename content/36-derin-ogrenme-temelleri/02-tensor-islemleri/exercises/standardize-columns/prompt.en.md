`standardize(rows)` should subtract each column's mean and divide by its
standard deviation (with broadcasting, no loops). Return the result as a list of
lists rounded to 3 places.

**Expected output:**

```
[[-1.0, -1.0], [0.0, 0.0], [1.0, 1.0]]
[[-0.707, 0.707], [0.707, -0.707]]
```
