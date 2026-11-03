`egcd(a, b)` should return `[g, x, y]`: `g = gcd(a, b)` and
`a * x + b * y == g`. It is recursive: when `b == 0`, `a = a * 1 + 0 * 0`,
so the base case is `[a, 1, 0]`. The starter code's base case is wrong.

**Expected output:**

```
1 4 -1
1
2 2
```
