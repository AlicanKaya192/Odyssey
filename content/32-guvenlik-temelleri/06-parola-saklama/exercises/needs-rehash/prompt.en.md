`needs_rehash(record, min_iterations)` should return `True` if a record
needs to be hashed again with new parameters:

- if the algorithm is not `"pbkdf2_sha256"`,
- if the record does not have 4 parts or the iteration count is not
  digits,
- if the iteration count is less than `min_iterations`.

The starter code compares the numbers **as text**: `"90000" < "600000"`
comes out `False`, because texts are compared character by character and
`"9"` is greater than `"6"`.

**Expected output:**

```
1000 True
90000 True
600000 False
1 True
```
