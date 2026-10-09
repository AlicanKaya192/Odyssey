Write the function `unique_path(path)`: if `path` (a `Path`) does not
exist, return it; otherwise return the first path that does **not** exist by
adding `-1`, `-2`... to the end of its name (`with_stem`, `exists`). While
`report.txt` and `report-1.txt` exist, the result is `report-2.txt`.

**Expected output:**

```
report-1.txt
report-2.txt
new.txt
```
