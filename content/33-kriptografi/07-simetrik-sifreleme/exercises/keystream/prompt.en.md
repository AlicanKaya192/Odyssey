`keystream(key_hex, nonce_hex, length)` should make a `length`-byte
keystream from the key and nonce: `counter` starts at 0, each block is
`sha256(key + nonce + counter.to_bytes(4, "big")).digest()`, blocks are
added until they pass `length` bytes, and the result is cut to `length`
bytes.

**Expected output:**

```
3addfb141c
10
40
0b4ce3c3
```
