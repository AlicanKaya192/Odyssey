Write the function `mask_log(lines, secrets)`. It should take a list of log lines, replace every secret in every line with `***` and return a new list.

Two rules:

- An empty secret (`""`) is skipped.
- **Longer** secrets are replaced first. Otherwise, once `abc123XYZ` is replaced first, the `abc123XYZ-backup` line keeps `***-backup` and part of the value leaks.

**Expected output:**

```
Login as admin
Using token ***
Retry with ***
Done
```
