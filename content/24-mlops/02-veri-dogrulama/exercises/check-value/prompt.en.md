Write the function `check_value(value, low, high)`. Ask the value these questions in order and return the first answer that applies:

- If the value is `None`, `"missing"`.
- If it is not a number (not an `int` or a `float`), `"not a number"`.
- If it is not between `low` and `high` (both ends included), `"out of range"`.
- Otherwise `"ok"`.

**Expected output:**

```
ok
missing
not a number
out of range
ok
```
