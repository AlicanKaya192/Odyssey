Write the function `linear_search(items, target)`: it goes through the list
from start to end and returns **a tuple of two values**: `(index, steps)`.

- `index`: where the value first appears; `-1` if missing.
- `steps`: the number of comparisons made (how many times
  `items[i] == target` was asked).

An empty list must give `(-1, 0)`.

**Expected output:**

```
(0, 1)
(1, 2)
(4, 5)
(-1, 5)
```

The best case is 1 step, the worst case (missing or at the end) `n` steps.
