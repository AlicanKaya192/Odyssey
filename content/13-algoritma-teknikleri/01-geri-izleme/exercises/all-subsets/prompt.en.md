Write the function `subsets(items)` **with backtracking**: it returns all
subsets in the order you saw in the lesson (at every node first add the
current path, then add one of the next elements and continue).

- `[1, 2, 3]` → `[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]`

No `itertools`.

**Expected output:**

```
[]
[1]
[1, 2]
[1, 2, 3]
[1, 3]
[2]
[2, 3]
[3]
1024
```
