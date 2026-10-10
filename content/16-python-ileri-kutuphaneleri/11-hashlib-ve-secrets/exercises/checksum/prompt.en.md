`checksum(path)` should return the SHA-256 digest (hexadecimal, full) of
the file's **content**. Open the file in binary mode (`"rb"`), read it in
4096-byte pieces and feed each piece with `update` (or use
`hashlib.file_digest`). The starter code hashes the file's **name**, not the
file.

**Expected output:**

```
a6a364ba6b5c813b
e3b0c44298fc1c14
```
