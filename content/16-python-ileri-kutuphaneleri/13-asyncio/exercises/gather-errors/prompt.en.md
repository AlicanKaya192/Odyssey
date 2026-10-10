`safe_all(values)` should run `check(value)` for every value together with
`gather` and return the results **in the given order**. Put `"error"` in
place of a value that failed. Use `return_exceptions=True`, then replace
those where `isinstance(result, Exception)`.

**Expected output:**

```
[10, 'error', 30]
```
