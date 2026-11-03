`toy_cipher` and `seal` are ready. `open_box(enc_key_hex, mac_key_hex,
box_hex)` should split the package (nonce 8, tag 32 bytes), recompute the
tag over nonce + ciphertext, and compare it with `hmac.compare_digest`. If
it does not match, return `"rejected"` and **do not decrypt at all**; if it
matches, return the plaintext as hex.

**Expected output:**

```
b'pay 100'
rejected
rejected
```
