The registry is a dictionary: under every model name there is a `"versions"` list (`{"version": ..., "file": ...}`) and an `"aliases"` dictionary (`{"production": 2}`). Write the function `resolve(registry, name, alias)` and return the **file path** of the version the alias points at.

- If the model name isn't in the registry, `None`.
- If there is no such alias, `None`.
- If there is no version with the number the alias points at, `None`.

**Expected output:**

```
models/churn-v2.pkl
models/churn-v1.pkl
None
None
```
