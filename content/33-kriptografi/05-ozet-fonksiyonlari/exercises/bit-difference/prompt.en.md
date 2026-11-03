Two digests are given as hex text. `bit_difference(a_hex, b_hex)`
should return how many bits differ between two digests of the same length:
turn them to bytes with `bytes.fromhex(...)` first, XOR, then count the
ones. Hint: turn them into one number with `int.from_bytes(data, "big")`
and `bin(...).count("1")`.

**Expected output:**

```
0
True
```
