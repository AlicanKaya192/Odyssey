`files` is file name → content (text), `lock` is file name → expected
SHA-256 (`hashlib.sha256(content.encode()).hexdigest()`).
`verify_downloads(files, lock)` should return one line per file, in
alphabetical order by name:

- `"<name>: ok"` if the hash matches,
- `"<name>: mismatch"` if it is in `lock` but does not match,
- `"<name>: not in lock"` if it is not in `lock`.

**Expected output:**

```
alpha-1.0.zip: ok
beta-2.1.zip: mismatch
gamma-0.3.zip: not in lock
```
