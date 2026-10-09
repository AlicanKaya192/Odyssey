Write the function `count_pairs(n)` **with two nested loops**: it counts
every **pair** (`i < j`) of the numbers from `0` to `n-1` once and returns
the count.

Then, for `n` values 10, 100 and 1000, print `n`, the counted number of pairs
and the result of the formula `n * (n - 1) // 2` on one line.

**Expected output:**

```
10 45 45
100 4950 4950
1000 499500 499500
```

The count matches the formula; when `n` grows 10 times, the work grows about
100 times: `O(n²)`.
