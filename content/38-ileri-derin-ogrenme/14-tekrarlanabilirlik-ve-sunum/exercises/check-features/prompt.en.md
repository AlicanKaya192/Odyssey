`check_features(values, n=6)` should check the input: if it is not a list or
its length is not `n`, return `"expected a list of 6 numbers"` (the number
from `n`); if any value is not finite, `"values must be finite numbers"`; if
valid, `"ok"`.

**Expected output:**

```
ok
expected a list of 6 numbers
values must be finite numbers
```
