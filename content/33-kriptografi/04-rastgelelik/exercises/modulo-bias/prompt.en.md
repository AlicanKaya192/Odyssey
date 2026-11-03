A byte gives the 256 values 0–255 with equal probability. `bias(n)`
should compute `b % n` for each of the 256 bytes, count how many times
each result comes out and return the list `[least, most]` (`1 <= n <=
256`).

If the two are equal, `b % n` is evenly spread; if they differ, there is
modulo bias. The starter code ignores the remainder with `256 // n`.

**Expected output:**

```
100 [2, 3]
16 [16, 16]
6 [42, 43]
```
