Write the sum of the numbers from 1 to `n` with two separate algorithms:

- `sum_loop(n)`: adds the numbers one by one with a `for` loop (do not use
  `sum()`).
- `sum_formula(n)`: finds it without a loop using `n * (n + 1) // 2`.

If `n` is 0, both must return `0`.

Then, for `n` values 10, 100 and 1000, print `n` and the two results on
each line.

**Expected output:**

```
10 55 55
100 5050 5050
1000 500500 500500
```

Both give the same result, but the loop does `n` additions while the
formula is always a handful of operations.
