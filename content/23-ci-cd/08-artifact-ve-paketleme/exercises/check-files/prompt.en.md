`manifest` is a dictionary holding the expected SHA-256 hash of each file, `files` the contents of the files you have (`name: text`). Write the function `check_files(manifest, files)`; it should return a list of these lines, in order:

- For each file in `manifest`: `"name: missing"` if you do not have it, `"name: changed"` if its hash differs, `"name: ok"` if it is the same.
- Then `"name: unexpected"` for each file in `files` that is not in `manifest`.

Use the ready-made `sha256_text` function for a text's hash.

**Expected output:**

```
app.py: ok
config.json: changed
data.csv: missing
notes.txt: unexpected
```
