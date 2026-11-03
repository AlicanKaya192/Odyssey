`toy_cipher` is ready. `seal(enc_key_hex, mac_key_hex, nonce_hex,
message_hex)` should encrypt the message and return the package as hex:
`nonce + cipher + tag`. The tag is HMAC-SHA256 with the key `mac_key`,
computed over the bytes of **the nonce and the ciphertext** (not the
plaintext). `hexdigest()` gives the tag as hex.

**Expected output:**

```
47 bytes
0000000000000000
49d2dfee644b43
```
