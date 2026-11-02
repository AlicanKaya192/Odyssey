Harmless toy "files" are in a dictionary: name → text content. `known`
is a list of the SHA-256 hashes (hex) of known bad samples.

`signature_scan(files, known)` should return, in alphabetical order, the
names of the files whose content hash (`hashlib.sha256(
content.encode()).hexdigest()`) is in the list. Turn the list into a set
first for fast lookup.

**Expected output:**

```
copy.bin
toy.bin
```
