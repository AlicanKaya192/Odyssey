Write the function `bloom_check(items, queries, bits, hashes)`: build a Bloom
filter of length `bits` (`bytearray(bits)`), add `items`, and return a list
holding `True` for "probably yes" and `False` for "definitely not" for each
query.

An item's positions: `h(item, s) % bits` for `s = 0..hashes − 1`. `h` is
ready.

**Expected output:**

```
[True, True, False]
15
```
