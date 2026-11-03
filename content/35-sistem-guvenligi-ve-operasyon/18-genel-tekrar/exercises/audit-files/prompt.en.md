Each file is `[path, mode, content]`; the mode is octal text such as
`"644"`. `audit_files(files)` should return two kinds of findings, in
alphabetical order: `"<path>: world-writable"` (the last digit of the mode
has the write bit: `int(mode[-1]) & 2`) and `"<path>: secret"` (a line,
stripped and lower-cased, starts with one of `SECRET_KEYS`; once per
file). The File Permissions and Secrets Management sections.

**Expected output:**

```
app/config.ini: secret
tmp/notes.txt: secret
tmp/notes.txt: world-writable
```
