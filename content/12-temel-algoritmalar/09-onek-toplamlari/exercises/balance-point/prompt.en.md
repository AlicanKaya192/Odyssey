Write the function `balance_index(values)`: it returns the **first** index
where the sum of the elements on its left equals the sum of those on its
right (the element at that index belongs to neither side); `-1` if there is
none.

- `[1, 7, 3, 6, 5, 6]` → `3` (left: 1 + 7 + 3 = 11, right: 5 + 6 = 11)

No nested loop is needed: find the whole total first. While walking the list,
accumulate the left sum; the right sum is `total - left - values[i]`.

**Expected output:**

```
3
-1
0
```
