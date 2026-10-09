Write the function `insert_position(items, target)` **with binary search**: it
returns the **leftmost** index in the sorted list where `target` can go
without breaking the order (where it first appears, if it is there).

- `[1, 3, 3, 5]`: `3` → `1`, `4` → `3`, `0` → `0`, `9` → `4`

The last line searches a list of a million elements 20,000 times; a linear
search hits the time limit. No `bisect` and no `index`.

**Expected output:**

```
3 1
4 3
0 0
9 4
10043050000
```
