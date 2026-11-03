`toy_cipher` is ready. `seal_aad(enc_key_hex, mac_key_hex, nonce_hex,
header_hex, message_hex)` should encrypt the message and return
`[cipher_hex, tag_hex]`. The header (AAD) is **not encrypted but goes into
the tag**: the signed bytes are, in order, `len(header).to_bytes(4, "big")`,
`header`, the nonce and the ciphertext. When the header changes, the tag
must change too.

**Expected output:**

```
True
False
```
