`decrypt_text(c, d, n, length)` should decrypt the number with `pow(c, d,
n)`, turn it into `length` bytes of text and return it with `decode()`. The
text was turned into a number with the `"big"` byte order; the starter code
uses `"little"` and the letters come out reversed.

**Expected output:**

```
hi!
ok
```
