Write the function `max_subarray(values)` with **Kadane**, in a single pass:
it returns the sum of the maximum subarray (consecutive, at least one
element).

`current` is the best sum ending here: `current = max(x, current + x)`;
`best` is the largest so far.

The last line has a million elements; an `O(n²)` solution that tries every
start–end pair hits the time limit.

**Expected output:**

```
7
-1
591
```
