Complete the function `karatsuba(x, y)`: it multiplies two non-negative
integers with **three** half-size multiplications.

- `half = max(len(str(x)), len(str(y))) // 2`
- `a, b = divmod(x, 10 ** half)`, `c, d = divmod(y, 10 ** half)`
- `ac`, `bd` and `(a + b)(c + d)` with recursion; the middle term is
  `(a + b)(c + d) - ac - bd`
- the result is `ac * 10 ** (2 * half) + middle * 10 ** half + bd`

The base case and the counter are ready: `MULTS` counts the single-digit
multiplications. `count_mults` catches a solution that uses four
multiplications.

**Expected output:**

```
7006652
True
33
```
