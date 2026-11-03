`keystream` is ready. `stream_encrypt(key_hex, nonce_hex, data_hex)`
should make a keystream as long as the data, XOR byte by byte, and return
the result as hex. The same operation is used for decryption (XOR is its
own inverse).

**Expected output:**

```
True
68656c6c6f
```
