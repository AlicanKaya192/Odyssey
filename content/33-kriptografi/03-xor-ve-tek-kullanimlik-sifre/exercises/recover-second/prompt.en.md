Two messages were encrypted with the **same** key; you do not know the
key but you know the first message. `recover_second(c1_hex, c2_hex,
first)` should return the second message as text: `c1 ^ c2 = m1 ^ m2`,
then XOR that with `first`. If the lengths differ, read as much as the
shorter one.

**Expected output:**

```
RETREAT AT TEN
```
