One way to watch integrity is to keep the fingerprints (hashes) of
files and compare them again later. `old` and `new` are two dictionaries
from file name to hash.

Write the function `integrity_changes(old, new)` and return this
dictionary:

- `"added"`: files only in `new`,
- `"removed"`: files only in `old`,
- `"changed"`: files in both whose hash is different.

Every list should be in alphabetical order with `sorted`.

**Expected output:**

```
added ['run.sh']
removed ['notes.txt']
changed ['config.ini']
```
