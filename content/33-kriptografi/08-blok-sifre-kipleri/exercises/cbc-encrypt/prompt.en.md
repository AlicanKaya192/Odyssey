`encrypt_block` is ready. `cbc_encrypt(key_hex, iv_hex, data_hex)` should
encrypt in CBC mode (the data is a multiple of 16 bytes): each block is
first XORed with `prev`, then encrypted, and **the ciphertext block becomes
the new `prev`**. The first `prev` is the IV. The result is hex. Two
identical blocks must give different ciphertext blocks.

**Expected output:**

```
False
32 bytes
```
