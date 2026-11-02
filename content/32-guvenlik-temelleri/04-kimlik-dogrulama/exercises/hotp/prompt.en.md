Turn the steps from the lesson into a function: `hotp(secret, counter,
digits=6)`.

- `secret` is text; turn it into bytes with `encode()` before giving it
  to HMAC.
- The counter becomes the message as an 8-byte big-endian (`"big"`)
  number.
- HMAC-SHA1, dynamic truncation, `& 0x7FFFFFFF`, `% 10**digits`.
- Return the result as **text** of length `digits` (`zfill`).

The standard's secret to test with: `"12345678901234567890"`.

**Expected output:**

```
0 755224
1 287082
2 359152
3 969429
94287082
```
