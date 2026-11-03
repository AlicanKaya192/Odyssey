**XOR.** `xor_hex(a_hex, b_hex)` should XOR two hex values byte by byte
and return hex; if their lengths differ, `"length mismatch"`. Because the
starter code uses `zip`, it silently stops at the end of the shorter one:
if a keystream were shorter than the message, part of the message would
stay unencrypted.

**Expected output:**

```
f00f
68656c6c6f
length mismatch
```
