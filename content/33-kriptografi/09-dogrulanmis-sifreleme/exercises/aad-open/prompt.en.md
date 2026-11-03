`toy_cipher` and `seal_aad` are ready. `open_aad(enc_key_hex,
mac_key_hex, nonce_hex, header_hex, cipher_hex, tag_hex)` computes the tag
correctly, but when it does not match it only prints a warning and
**decrypts anyway**. Fix it: if the tag does not match, return
`"rejected"` without decrypting; if it matches, give the plaintext as
hex.

**Expected output:**

```
b'pay 100'
rejected
```
