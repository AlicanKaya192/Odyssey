Write the function `ks_statistic(a, b)` that computes the KS statistic between two samples:

- Sort both lists.
- For every distinct value `x` in either list, find the share of values less than or equal to `x` in each list (`bisect.bisect_right(list, x) / len(list)`).
- Return the largest difference between the two shares, rounded to three digits.

**Expected output:**

```
0
0.4
0.667
```
