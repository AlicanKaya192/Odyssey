**Hash functions.** `manifest` maps each file name to its expected SHA-256
hash (hex); `files` maps a name to its content. `changed_files(files,
manifest)` should return, as a sorted list, the names from the manifest
that are **missing or whose content has changed**. A content's hash is
`hashlib.sha256(content.encode()).hexdigest()`. The starter code only finds
the missing ones.

**Expected output:**

```
['config.json', 'readme.md']
```
