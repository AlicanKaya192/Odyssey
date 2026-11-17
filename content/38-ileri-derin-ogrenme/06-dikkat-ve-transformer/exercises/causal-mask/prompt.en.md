`causal_mask(n)` should return the `n × n` boolean causal mask as a list:
`True` above the diagonal (do not look), `False` on and below it.

**Expected output:**

```
[False, True, True, True]
[False, False, True, True]
[False, False, False, True]
[False, False, False, False]
```
