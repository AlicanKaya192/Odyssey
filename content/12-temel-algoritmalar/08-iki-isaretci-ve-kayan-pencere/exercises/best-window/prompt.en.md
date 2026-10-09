Write the function `best_window(values, k)` **with a sliding window**: it
returns the largest sum of `k` consecutive values. If `k` is larger than the
list, `None`.

Sum the first window; then at every step add the one coming in and subtract
the one going out.

**Speed requirement:** at the end of the code a 5 000-day window is searched
for in 200 000 days of data; the time limit is 10 seconds. Summing every
window from scratch means about a billion additions.

**Expected output:**

```
16
None
256558
```
