Write the function `sum_digits(n)` **recursively**: it returns the sum of the
digits of a non-negative integer. Do not use a loop.

- `sum_digits(1234)` → `10`

**Three questions:**

1. The smallest form: if `n` has one digit (`n < 10`), the answer is `n`.
2. One step smaller: the last digit is `n % 10`, the rest is `n // 10`.
3. Combining: the last digit + the digit sum of the rest.

**Expected output:**

```
10
7
45
```
