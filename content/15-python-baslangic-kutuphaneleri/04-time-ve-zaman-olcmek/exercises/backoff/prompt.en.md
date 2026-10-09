Write the function `backoff(n, base, cap)`: return the waiting times of the
first `n` attempts of exponential backoff as a list. The `i`th time is
`base * 2 ** i` (i starts at 0), but none may exceed `cap`.
Example: `backoff(5, 1, 10)` → `[1, 2, 4, 8, 10]`.

**Expected output:**

```
[1, 2, 4, 8, 10]
[0.5, 1.0, 2.0, 4.0]
```
