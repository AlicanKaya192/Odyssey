`check_pair(e, d, n, samples)` should test whether a key pair is right:
for every `m` in `samples`, `pow(pow(m, e, n), d, n) == m` must hold; if
even one fails, `False`. The starter code looks at `e * d % n`; but the
inverse is taken mod `phi`, not mod `n`, so even a right pair is
rejected.

**Expected output:**

```
True
False
```
