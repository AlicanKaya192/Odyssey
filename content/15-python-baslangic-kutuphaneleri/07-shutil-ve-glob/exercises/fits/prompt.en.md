There is a `media` folder next to your file (three files with its
subfolder).

Write the function `fits(folder, free)`: find the total size of all files in
the folder in bytes (`rglob`, `stat().st_size`) and return the tuple
`(total, total <= free)`. In real use the `free` value comes from
`shutil.disk_usage(...).free`.

**Expected output:**

```
(18, True)
(18, False)
```
