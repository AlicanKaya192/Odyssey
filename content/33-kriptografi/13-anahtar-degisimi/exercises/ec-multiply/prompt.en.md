`add` is ready (points are `[x, y]` lists, the point at infinity is
`None`). `mul(k, pt)` should compute `k·pt` with **double and add**: if the
last binary digit of `k` is 1, `pt` is added to the result; every round
`pt` is added to itself (doubled), and `k` shifts one digit to the right.
The doubling line is missing from the starter code.

**Expected output:**

```
[0, 2]
True
True
None
```
