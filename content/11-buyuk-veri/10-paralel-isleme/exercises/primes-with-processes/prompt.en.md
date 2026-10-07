Count the primes between 0 and 100 000 by splitting them into four pieces
with a process pool, and compare the result with the sequential solution.

**What to do:**

1. The `count_primes` function is ready in the starter code.
2. Inside the `if __name__ == "__main__":` block:
   - `parts = [(i * 25_000, (i + 1) * 25_000) for i in range(4)]`,
   - take the result of `ex.map(count_primes, parts)` with
     `ProcessPoolExecutor(max_workers=2)` into a list and print it,
   - print the total,
   - work out the same total sequentially (`sum(map(count_primes, parts))`)
     and print whether the two totals are equal.

**Expected output:**

```
[2762, 2371, 2260, 2199]
9592
True
```
