Python's `hash()` is reliable within a process, but for strings it **changes
on every run**. To write the value to a file, to expect two programs to give
the same result, or to split data into parts in a fixed way, a **stable** hash
is needed.

## `zlib.crc32`: fast and stable

```python
import zlib

key = "Istanbul"
print(zlib.crc32(key.encode("utf-8")))          # the same number on every run
print(zlib.crc32(key.encode("utf-8")) % 4)      # which of 4 parts?
```

We used this in the Big Data path to distribute data among workers. It is fast
but **not for security**: deliberately finding two strings with the same value
is easy.

## `hashlib`: a fingerprint

```python
import hashlib

content = "merhaba dunya".encode("utf-8")
print(hashlib.sha256(content).hexdigest()[:16])   # the first 16 of 64 characters
```

SHA-256 makes it practically impossible for two different contents to give
the same result. Uses: telling whether a file has changed (Odyssey's update
records also keep each file's SHA-256), finding duplicate files, verifying a
downloaded file.

## Which one when?

| Need | Tool |
|---|---|
| A set/dictionary within one process | the built-in `hash()` (automatically) |
| Splitting data into `n` parts in a fixed way | `zlib.crc32(...) % n` |
| A content fingerprint, an integrity check | `hashlib.sha256` |
| Storing passwords | none of them alone: salted, slow special functions (`hashlib.pbkdf2_hmac`; we used it in API 2) |

**Note:** `hashlib` and `crc32` want **bytes**, not a string; forgetting
`encode("utf-8")` gives a `TypeError`.
