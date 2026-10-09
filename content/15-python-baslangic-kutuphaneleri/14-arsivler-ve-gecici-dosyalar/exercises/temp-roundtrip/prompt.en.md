Write the function `temp_roundtrip(files)`: `files` is a `{name: text}`
dictionary. Open a temporary folder with `tempfile.TemporaryDirectory()`,
write every file into it and, inside the block, take the names in the folder
as a sorted list. After leaving the block, check whether the folder still
exists and return `(names, exists)`. The result must be `([...], False)`.

**Expected output:**

```
(['a.txt', 'b.txt'], False)
```
