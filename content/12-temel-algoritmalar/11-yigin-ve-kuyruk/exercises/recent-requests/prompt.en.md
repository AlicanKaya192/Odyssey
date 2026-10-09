The times of requests arriving at a server (seconds, in increasing order) are
given. Write the function `recent_counts(times, window)`: when each request
arrives, it records how many requests came in **the last `window` seconds**
(including now, those greater than `t - window`), and returns the counts in a
list.

- `recent_counts([1, 2, 5, 12, 13], 10)` → `[1, 2, 3, 2, 3]`
  (when 12 arrives, 1 and 2 have left the window: 5 and 12 remain)

Keep a **queue** (`deque`): add the new time at the end, drop the ones that
left the window from the front (`popleft`). Do not use `pop(0)` on a list.

**Expected output:**

```
[1, 2, 3, 2, 3]
[]
```
