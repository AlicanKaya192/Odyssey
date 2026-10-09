Write the function `parse_all(values, base)`: convert the strings to
integers in the given base and return them as a list. Build a one-argument
converter with `partial(int, base=base)` and apply it with `map`.

**Expected output:**

```
[255, 16, 7]
[5, 3]
```
