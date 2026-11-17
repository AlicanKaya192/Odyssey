`padding_mask(ids, pad)` should return a mask that can be given as
`key_padding_mask`: `True` where the padding id (`pad`) is, `False` at real
ids.

**Expected output:**

```
[False, False, True, True]
[False, False, False, True]
```
