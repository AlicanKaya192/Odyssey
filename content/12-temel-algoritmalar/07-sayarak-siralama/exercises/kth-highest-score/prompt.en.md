Write the function `kth_highest(scores, k)`: in a list of scores between 0
and 100, it returns the **k-th highest** score (repeats count separately).

- `kth_highest([70, 95, 80, 95, 60], 1)` → `95`
- `kth_highest([70, 95, 80, 95, 60], 3)` → `80` (95, 95, 80)

Do not sort the whole list: build 101 counters, walk them **down from 100**
and return the score when the number of scores passed reaches `k`. If `k` is
larger than the list, `None`.

Do not use `sorted` or `.sort()`.

**Expected output:**

```
95
80
None
```
