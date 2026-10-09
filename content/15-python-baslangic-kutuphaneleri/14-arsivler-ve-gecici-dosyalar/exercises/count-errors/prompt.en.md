Write the function `count_errors(path)`: without unpacking the `.gz`
compressed log file to disk first, read it line by line with
`gzip.open(path, "rt", encoding="utf-8")` and count the lines starting with
`ERROR`. The lines below create the file.

**Expected output:**

```
3
```
