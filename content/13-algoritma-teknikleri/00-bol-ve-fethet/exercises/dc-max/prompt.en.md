Write the function `dc_max(values, lo=0, hi=None)` **without loops, with divide
and conquer**: it returns the largest value in the range `values[lo..hi]`.

- A single element (`lo == hi`): that element.
- Otherwise split in the middle, get the answers of the two halves and
  return the larger one.

No `max`, `for` or `while`; the list is not empty.

**Expected output:**

```
9
-1
```
