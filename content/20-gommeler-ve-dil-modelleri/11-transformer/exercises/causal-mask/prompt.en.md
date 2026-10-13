`causal_mask(n)` should return an `n × n` mask: element `j` of row `i` is `1` if
word `j` can be looked at (`j <= i`), else `0`.

**Expected output:**

```
[1, 0, 0, 0]
[1, 1, 0, 0]
[1, 1, 1, 0]
[1, 1, 1, 1]
```
