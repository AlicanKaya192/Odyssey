Write the function `max_window_sum(values, k)` **with a sliding window**: it
returns the largest of the sums of `k` **consecutive** elements. `None` if
`k <= 0` or `k` is larger than the list.

- `[2, -1, 3, 5, -2, 4]`, `k = 3`: the windows are `4`, `7`, `6`, `7` → `7`

The large input on the last line makes an `O(n²)` solution hit the time limit; `O(n)` is needed. Summing each window from scratch with `sum` is `O(n × k)`.

**Expected output:**

```
7
None
1659
```
