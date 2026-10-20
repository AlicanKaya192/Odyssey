Write a small content-addressed store. The store is a dictionary: `{"objects": {hash: text}, "names": {name: hash}}`.

The function `add(store, name, text)` should:

- Compute the text's hash (SHA-256 of its UTF-8 bytes, the whole hexadecimal form).
- Set `store["names"][name]` to this hash (the name is always recorded).
- If the hash is already in `store["objects"]`, **not store** the text again and return `"already stored"`.
- Otherwise write `store["objects"][hash] = text` and return `"stored"`.

**Expected output:**

```
stored
stored
already stored
names: 3 objects: 2
```
