Write the function `make_pointer(name, text)` that builds the pointer file of a text file. Return a dictionary:

- `"path"`: the file's name (`name`).
- `"sha256"`: the SHA-256 hash of the text's UTF-8 bytes, the **whole** hexadecimal form (64 characters).
- `"size"`: the number of bytes.

The same contents give the same hash even under a different name.

**Expected output:**

```
notes.txt 5
2cf24dba5fb0
64
True
```
