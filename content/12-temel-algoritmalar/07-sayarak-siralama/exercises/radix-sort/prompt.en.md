Write the function `radix_sort(items)`: it sorts a list of non-negative
integers digit by digit (ones, tens, hundreds…) with 10 buckets.

1. An empty list comes back empty.
2. Start with `place = 1`; do rounds while `max(items) // place > 0`.
3. In each round build 10 empty buckets; add each number to bucket
   `(x // place) % 10`.
4. Collect the buckets in order from 0 to 9; `place *= 10`.

Do not use `sorted` or `.sort()`.

**Expected output:**

```
[2, 24, 45, 66, 75, 90, 170, 802]
[1, 3, 5, 5]
```
