Each program is a dict: `name` and protection names → `True` / `False`.
The required protections are `canary`, `nx`, `pie`.
`missing_protections(binary)` should return the missing ones as a list in
alphabetical order. A protection that is **absent** from the dict also
counts as missing (it is checked, not assumed).

**Expected output:**

```
app: ok
tool: canary, pie
old: canary, nx, pie
```
