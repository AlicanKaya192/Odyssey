`checked_add(a, b, bits)` should add two sizes and return the result if
it fits in a `bits`-bit number (is smaller than `2 ** bits`), or `None` if
it does not. The starter code behaves like C and wraps around: that leads
to a small region being reserved.

**Expected output:**

```
255
None
None
300
```
