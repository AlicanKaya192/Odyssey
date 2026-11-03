`unexpected_setuid(files, allowed)` should return, in alphabetical order,
the paths of files whose setuid bit is on (`mode & 0o4000`) and that are
not in the `allowed` list.

**Expected output:**

```
/opt/app/helper
/opt/tools/report-tool
```
