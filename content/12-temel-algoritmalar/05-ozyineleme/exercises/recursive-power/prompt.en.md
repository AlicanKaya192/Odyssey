Write the function `power(base, exp)` **recursively**: it returns `base`
raised to the power `exp` (`exp >= 0` integer).

- `power(2, 10)` → `1024`
- `power(5, 0)` → `1`

**Rules:** do not use the `**` operator, the `pow` function or a loop. The
base case is `exp == 0`; the step is `base * power(base, exp - 1)`.

**Expected output:**

```
1024
1
81
```
