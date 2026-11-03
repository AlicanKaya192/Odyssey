`hash_strength(name)` should return the strength of a hash name (case
does not matter):

- `md5`, `sha1` → `"weak"`
- `sha256`, `sha512`, `sha3_256`, `blake2b` → `"strong"`
- anything else → `"unknown"`

**Expected output:**

```
md5 weak
SHA1 weak
sha256 strong
blake2b strong
rot13 unknown
```
