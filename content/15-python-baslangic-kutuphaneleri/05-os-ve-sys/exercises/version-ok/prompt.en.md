Write the function `version_ok(info, minimum)`: `info` is a version
(`(3, 14, 7)` or `sys.version_info`), `minimum` the lowest version
(`(3, 10)`). Return `True` if the first `len(minimum)` parts of `info` are
equal to or greater than `minimum`. Turn both into `tuple(...)` and
compare.

**Expected output:**

```
True
False
True
```
