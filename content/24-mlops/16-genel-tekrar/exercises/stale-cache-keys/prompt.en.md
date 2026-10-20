Cache keys look like `"customer@version"` (`"C1@v2"`). Write the function `stale_keys(keys, live_version)` that finds the entries gone stale when the live model changes:

- Split every key into customer and version with `"@"`.
- Return, in order, the **customers** of those whose version isn't `live_version`.

**Expected output:**

```
['C1', 'C3']
['C2', 'C4']
[]
```
