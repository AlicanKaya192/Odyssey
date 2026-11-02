`hotp` is ready. `verify_code(secret, code, unix_time)` should check the
code the user typed:

- The current counter is `unix_time // 30`.
- Against clock drift, accept the three codes produced for counter `- 1`,
  the counter itself and `+ 1`.
- Compare with `hmac.compare_digest(a, b)`, not `==`: `==` stops at the
  first different character and the time taken can give a hint;
  `compare_digest` always compares the whole text.

Return `True` if one matches, otherwise `False`.

**Expected output:**

```
True
True
False
False
```
