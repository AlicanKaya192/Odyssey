The contents of a file that came back from the store (`text`) and its pointer file (`pointer`: `"path"`, `"sha256"`, `"size"`) are given. Write the function `verify(pointer, text)`:

- If the number of the text's UTF-8 bytes is not `pointer["size"]`, return `"size mismatch"`. Measuring the size is cheap; look at it first.
- If the size matches but the SHA-256 hash (the whole hexadecimal form) is not `pointer["sha256"]`, `"hash mismatch"`.
- If both match, `"ok"`.

**Expected output:**

```
ok
size mismatch
hash mismatch
```
