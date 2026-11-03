`mod_pow(base, exp, mod)` should compute `base ** exp % mod` with
**square and multiply**; `pow` is not used. One line is missing from the
starter code: every round the base must be multiplied by itself and
reduced (`base = base * base % mod`).

**Expected output:**

```
3
1
24
```
