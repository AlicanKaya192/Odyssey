Write two functions:

- `parse_version(text)`: turn a version such as `"2.4.10"` into a
  **tuple** of numbers: `(2, 4, 10)`.
- `needs_patch(installed, fixed)`: return `True` if the installed version
  is **older** than the fixed version. Compare tuples; text comparison
  takes `2.4.10` to be smaller than `2.4.9`.

**Expected output:**

```
(2, 4, 10)
True
False
False
False
```
