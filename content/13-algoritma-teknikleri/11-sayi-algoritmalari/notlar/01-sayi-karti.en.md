## What Python has ready

| What | How | Note |
|---|---|---|
| GCD / LCM | `math.gcd(a, b)`, `math.lcm(a, b)` | `math.lcm(4, 6)` = 12 |
| Integer square root | `math.isqrt(n)` | `int(n ** 0.5)` can be wrong for big numbers |
| Power with mod | `pow(a, e, m)` | fast exponentiation |
| Modular inverse | `pow(a, -1, m)` | `pow(3, -1, 7)` = 5, because `3 × 5 % 7 = 1` |
| Quotient and remainder | `divmod(a, b)` | `divmod(17, 5)` = `(3, 2)` |

## Costs

| Algorithm | Cost |
|---|---|
| Euclid | `O(log min(a, b))` |
| Primality (up to the square root) | `O(√n)` |
| Sieve (all primes up to `n`) | `O(n log log n)` time, `O(n)` memory |
| Fast exponentiation | `O(log e)` multiplications |

## Common mistakes

- A floating-point square root: for `n = (10**8 + 1)**2 - 1`, `int(n ** 0.5)`
  gives 100000001, the right answer is 100000000 (`math.isqrt`).
- Computing the huge number first and taking mod afterwards:
  `3 ** 1_000_000 % m` is right but builds an intermediate number with hundreds
  of thousands of digits; `pow(3, 1_000_000, m)` does not.
- The mod of a negative number: in Python `-7 % 3` = 2 (the result is always
  `0`..`m − 1`); other languages may give `-1`.
- Starting the sieve's inner loop at `2 * p` is not wrong but wasteful:
  multiples below `p * p` were already marked by smaller primes.
