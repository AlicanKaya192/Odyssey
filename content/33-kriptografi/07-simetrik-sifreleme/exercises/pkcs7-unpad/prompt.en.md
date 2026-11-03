`pad` is ready. `unpad(data_hex)` should remove PKCS#7 padding and
return the result as hex: get the bytes with `bytes.fromhex`, the last byte
says how many padding bytes were added, drop that many from the end. Hint:
`data[:-data[-1]]`.

**Expected output:**

```
True
True
```
