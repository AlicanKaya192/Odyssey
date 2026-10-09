A practical way to find an algorithm's class by measuring is the **doubling
test**: double the input and see how many times bigger the work gets.

1. Write the function `count_triples(n)` **with three nested loops**: it
   counts every **triple** `i < j < k` of the numbers from `0` to `n-1` once.
2. For `n` values 10, 20, 40 and 80, print `n`, the number of triples and the
   ratio to the previous `n` (`new / old`, with `round(..., 2)`). The first
   line has no ratio.

**Expected output:**

```
10 120
20 1140 9.5
40 9880 8.67
80 82160 8.32
```

The ratio approaches 8: `2³ = 8`. Three nested loops are `O(n³)`.
