Memory is a list of numbers: the first 8 are the name field, the last 4
the role. `copy_bounded(memory, start, size, data)` should return a
**copy** of the memory; it should copy at most `size` numbers of `data`
starting at index `start` and drop the rest. The starter code writes the
extra too and damages the role.

**Expected output:**

```
[1, 2, 3, 0, 0, 0, 0, 0]
[85, 83, 69, 82]
[1, 2, 3, 4, 5, 6, 7, 8]
[85, 83, 69, 82]
```
