`xor_hex(a_hex, b_hex)` should XOR two byte strings written in hex,
byte by byte, and return the result as hex text again. If their lengths
differ, return `None` (`zip` silently stops at the shorter one, so check
first).

**Expected output:**

```
f0f0
0000
None
```
