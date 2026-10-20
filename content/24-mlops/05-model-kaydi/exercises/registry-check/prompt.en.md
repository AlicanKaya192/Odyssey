A model's registry entry (`entry`) and the files on disk (`disk`: file path → hash) are given. Write the function `check_registry(entry, disk)` and return the list of problems:

1. First the aliases, in dictionary order: if there is no version with the number the alias points at, `"<alias>: version <n> does not exist"`.
2. Then the versions, in list order: if the file isn't on disk, `"v<n>: file missing"`; if it is but its hash differs from the registry's, `"v<n>: hash mismatch"`.

If there are no problems, an empty list.

**Expected output:**

```
staging: version 4 does not exist
v2: hash mismatch
v3: file missing
```
