## Operations

| Operation | Python | Example | Result |
|---|---|---|---|
| Remainder | `a % n` | `27 % 12` | 3 |
| Addition mod n | `(a + b) % n` | `(10 + 5) % 12` | 3 |
| Multiplication mod n | `(a * b) % n` | `(7 * 8) % 12` | 8 |
| Big power | `pow(a, e, n)` | `pow(7, 128, 13)` | 3 |
| Gcd | `math.gcd(a, b)` | `math.gcd(12, 18)` | 6 |
| Inverse | `pow(a, -1, n)` | `pow(3, -1, 11)` | 4 |

## Rules

- In Python `a % n` is always between `0` and `n - 1` (also for negative `a`).
- Taking `% n` at intermediate steps does not change the result; the numbers
  stay small.
- **Always** `pow(a, e, n)` instead of `a ** e % n`: same result, much faster.
- An inverse exists only if `gcd(a, n) == 1`; otherwise `pow` raises
  `ValueError`.

## Square and multiply

```text
result = 1
while exp > 0:
    if the last binary digit of exp is 1: result = result × base mod n
    base = base × base mod n
    shift exp one digit to the right
```

The number of rounds is the number of **binary digits** of the exponent
(7 for 117).

## Extended Euclid

`egcd(a, b)` → `(g, x, y)` such that `a·x + b·y = g`. If `g == 1`, `x % b`
is the inverse of `a` mod `b`.

## Fermat's little theorem

If `p` is prime and `a % p != 0`, then `pow(a, p - 1, p) == 1`.
