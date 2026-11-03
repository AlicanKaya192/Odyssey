Each file is a dict: `path`, `mode`, `secret` (does it hold a secret).
`audit_files(files)` should return the findings line by line, in
alphabetical order by path:

- `"<path>: world-writable"` if `mode & 0o002`,
- `"<path>: secret exposed"` if `secret` is true and `mode & 0o077`.

If a file has both, `world-writable` comes first.

**Expected output:**

```
/home/ada/.env: secret exposed
/srv/app/config.ini: world-writable
/tmp/notes.txt: world-writable
/tmp/notes.txt: secret exposed
```
