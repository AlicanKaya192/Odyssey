`run_all(values)` should give each value to the pool with
`pool.submit(check, value)` and return the results **in input order** in a
list. `check` raises a `ValueError` for negative numbers; put the text
`"error"` in the list in that value's place. The starter code does not catch
the error, so it fails completely.

**Expected output:**

```
[10, 'error', 30]
[]
```
