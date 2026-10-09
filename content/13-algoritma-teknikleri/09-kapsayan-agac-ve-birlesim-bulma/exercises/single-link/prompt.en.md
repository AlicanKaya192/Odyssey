Write the function `clusters(points, k)`: it splits the points into `k`
groups with **single-linkage clustering**. Sort all pairs of points by
distance (`math.dist`), merge them with union-find; stop when the number of
groups drops to `k`.

Return: each group is a sorted list of the points' **indices**, and the groups
are sorted by their first index.

**Expected output:**

```
[0, 1, 2]
[3, 4, 7]
[5, 6]
[[0, 1, 2, 3, 4, 5, 6, 7]]
```
