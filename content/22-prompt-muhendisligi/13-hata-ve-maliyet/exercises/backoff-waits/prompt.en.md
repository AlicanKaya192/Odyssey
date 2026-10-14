`backoff_waits(attempts, base, cap)` should return the waits between
`attempts` attempts as a list: `attempts - 1` waits, the `i`-th wait is
`base * 2 ** i`, but none may be larger than `cap`.

**Expected output:**

```
[1.0, 2.0, 4.0]
[0.5, 1.0, 2.0, 4.0, 8.0, 8.0]
[]
```
