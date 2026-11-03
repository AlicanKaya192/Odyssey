`hkdf_extract` and `hkdf_expand` are ready. `derive_pair(master_hex,
salt_hex)` should derive two 32-byte keys from the master secret, one for
encryption and one for the MAC, and return `[enc_hex, mac_hex]`. The starter
code uses the same `info` label for both, so the two keys come out equal.
The encryption key's label should be `b"encryption"`, the MAC key's
`b"mac"`.

**Expected output:**

```
False
32 32
```
