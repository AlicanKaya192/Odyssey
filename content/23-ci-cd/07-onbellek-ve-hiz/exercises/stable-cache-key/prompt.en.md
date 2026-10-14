Write the function `cache_key(tool, runner_os, requirements)`. It should return a key like `"pip-Linux-1a2b3c4d"`: the tool, the operating system and the first 8 characters of the content's SHA-256 hash.

One more condition: if only the **order of the lines** or **blank lines** differ, the key must not change. For this, before hashing:

- Split the text into lines, strip the spaces at the start and end of each line, drop the blank lines.
- Sort the lines and join them with `"\n"`.

The hash: `hashlib.sha256(text.encode()).hexdigest()`.

**Expected output:**

```
pip-Linux-509b0a14
pip-Linux-509b0a14
pip-Linux-9c118a73
```
