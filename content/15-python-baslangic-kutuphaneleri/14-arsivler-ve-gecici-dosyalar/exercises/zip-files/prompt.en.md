There are `a.txt`, `b.txt` and `data/c.csv` next to your file. Write the
function `zip_files(zip_path, paths)`: put the files in `paths` into the
`zip_path` archive **compressed** (`ZIP_DEFLATED`), then open the archive and
return the names inside as a **sorted** list.

**Expected output:**

```
['a.txt', 'data/c.csv']
```
