The first bytes of files are given as hex text. Two functions:

- `file_kind(header_hex)`: if it starts with `25504446` → `"pdf"`,
  `89504e47` → `"png"`, `504b0304` → `"zip"`, that type, otherwise
  `"unknown"` (case does not matter).
- `mismatches(files)`: name → hex header; return, in alphabetical order,
  the names of files whose type is known but does not match the
  extension.

**Expected output:**

```
pdf
zip
unknown
['photo.png']
```
