`hash_hex(text, name)` should hash the text (turned to bytes with
`encode()`) with the `name` algorithm and return the digest as hex text.
Use `hashlib.new(name, ...)`.

**Expected output:**

```
50a8d1d0939b05a7
True
40 32
```
