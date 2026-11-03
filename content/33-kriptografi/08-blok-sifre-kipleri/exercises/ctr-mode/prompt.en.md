`encrypt_block` is ready. `ctr_crypt(key_hex, nonce_hex, data_hex)` should
encrypt or decrypt in CTR mode: for block `n` the counter block is
`nonce_hex + n.to_bytes(8, "big").hex()`, this block is encrypted, and the
resulting keystream is XORed with that block of the data. The last block
may be short; there is no padding. The result is hex.

**Expected output:**

```
35 bytes
False
b'the same block!!the same block!!end'
```
