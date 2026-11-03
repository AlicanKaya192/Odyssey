`hkdf_extract` and `hkdf_expand` are ready. `keys_from_password(password,
salt_hex, iterations)` should derive an encryption key and a MAC key from a
password. The starter code gives the password's bytes directly to HKDF;
since HKDF is fast, this does not protect the password. A slow KDF first:
`master` with PBKDF2-SHA256 (`salt`, `iterations`, `dklen=32`); then
`hkdf_extract` with the same salt and `hkdf_expand` with the two labels.
The result is `[enc_hex, mac_hex]`.

**Expected output:**

```
False
False
True
```
