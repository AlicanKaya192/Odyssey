`causal_mask(n)` should return an `n × n` boolean mask: the **future**
positions a position must not see (column > row) are `True`, the others
`False`.

**Expected output:**

```
[False, True, True]
[False, False, True]
[False, False, False]
```
