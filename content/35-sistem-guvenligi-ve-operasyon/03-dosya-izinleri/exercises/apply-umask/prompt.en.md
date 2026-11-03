`apply_umask(base, umask)` should **remove** the umask's bits from the
permission the program asks for (`base`). The starter code subtracts:
`0o666 - 0o022` happens to come out right but `0o666 - 0o077` does not
give `0o600`. Write it with a bit operation: `base & ~umask`.

**Expected output:**

```
0o644
0o600
0o750
```
