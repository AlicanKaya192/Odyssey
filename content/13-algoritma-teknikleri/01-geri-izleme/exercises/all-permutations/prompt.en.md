Write the function `permutations(items)` **with backtracking**: it returns
every ordering of the list as a list of lists. Order: at each step try the
unused elements **in their order in the list**.

- `[1, 2, 3]` → `[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]`

Mark the used ones in a `used` list; do not forget to clear the flag when
undoing. No `itertools`.

**Expected output:**

```
[1, 2, 3]
[1, 3, 2]
[2, 1, 3]
[2, 3, 1]
[3, 1, 2]
[3, 2, 1]
5040
```
