`files` is name → content (text), `known` is name → expected SHA-256
(hex). The content's digest is `hashlib.sha256(content.encode()).hexdigest()`.
`file_report(files, known)` should return one line per file, in
alphabetical order:

- `"<name> ok"` if the digest matches the value in `known`,
- `"<name> changed"` if it is in `known` but the digest does not match,
- `"<name> unknown"` if it is not in `known`.

**Expected output:**

```
a.txt ok
b.txt changed
c.txt unknown
```
