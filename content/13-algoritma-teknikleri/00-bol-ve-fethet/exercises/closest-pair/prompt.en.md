Write the function `closest(points)` **with divide and conquer**: it returns
the distance of the closest pair of points sorted by `x`.

1. At most 3 points: look at every pair (`math.dist`).
2. Split in the middle (`mid_x = points[mid][0]`), solve the two halves, the
   smaller is `d`.
3. Sort those with `abs(x - mid_x) < d` by `y`; for each point look at the
   following ones, stop when the `y` difference exceeds `d`.

`closest_distance` sorts and rounds the result. The 30,000 points on the
last line make brute force (450 million distances) hit the time limit.

**Expected output:**

```
1.0
28.79236
```
