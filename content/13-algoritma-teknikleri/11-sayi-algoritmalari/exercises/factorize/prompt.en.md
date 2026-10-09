Write the function `factorize(n)`: it returns the prime factors of `n` from
smallest to largest, with repeats, as a list (`360` → `[2, 2, 2, 3, 3, 5]`).

Start `d` at 2; while `d` divides, divide and add it to the list. Only try
while `d * d <= n`: when the loop ends, if `n` is still above 1 it is a prime
factor too. On the billion-sized prime on the last line, trying up to `n` runs
out of time.

**Expected output:**

```
[2, 2, 2, 3, 3, 5]
[97]
[1000000007]
```
