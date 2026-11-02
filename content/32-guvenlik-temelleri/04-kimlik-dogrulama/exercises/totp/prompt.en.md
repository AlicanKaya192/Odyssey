`hotp` is ready in the starter code. TOTP is HOTP using the clock instead
of a counter.

Write the function `totp(secret, unix_time, step=30, digits=6)`: the
counter is `unix_time // step`, the code is `hotp(secret, counter, digits)`.

**Expected output:**

```
59 287082
1111111109 081804
1234567890 005924
94287082
```
