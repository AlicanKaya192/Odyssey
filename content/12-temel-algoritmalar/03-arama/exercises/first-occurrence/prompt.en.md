Write the function `first_occurrence(items, target)`: in a sorted list that
may contain repeats, it finds the index of the **first** occurrence of
`target` with binary search; `-1` if missing.

- `3` in `[1, 3, 3, 3, 5]` → `1`

Do not stop at a match: note the answer (`answer = mid`) and keep searching
**left** (`hi = mid - 1`).

**Rules:** do not use `.index()` or `bisect`.

**Expected output:**

```
1
4
-1
```
