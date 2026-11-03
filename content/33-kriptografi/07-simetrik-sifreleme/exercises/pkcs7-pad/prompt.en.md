`pad(data_hex, block)` should add PKCS#7 padding to hex data and return
the result as hex. `bytes.fromhex` first; the number of missing bytes is
`need = block - (len(data) % block)`; `need` bytes, each with the value
`need`, are added. If the data is already a multiple of a block, **a whole
new block** is still added (`need` is `block`, not 0).

**Expected output:**

```
5 -> 16 last: 11
16 -> 32 last: 16
```
