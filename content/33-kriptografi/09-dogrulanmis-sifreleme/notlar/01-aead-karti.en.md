## What it provides

| Property | Encryption only | MAC only | Authenticated encryption |
|---|---|---|---|
| Confidentiality | Yes | No | Yes |
| Integrity | No | Yes | Yes |
| Source authentication (whoever knows the key) | No | Yes | Yes |

## Encrypt-then-MAC

1. Encrypt the plaintext with a nonce: `cipher = encrypt(enc_key, nonce, message)`.
2. Compute the tag over **nonce + ciphertext**:
   `tag = hmac(mac_key, nonce + cipher)`.
3. Send: `nonce + cipher + tag`.

The receiver:

1. Split the package: nonce, ciphertext, tag (the last 32 bytes).
2. Recompute the tag and compare it with `hmac.compare_digest`.
3. If it does not match, **stop**; if it matches, decrypt.

## Keys

- The encryption key and the MAC key are **separate**.
- Both can be derived from one master secret (the Key Derivation section).

## AAD

- Not hidden, but goes into the tag: if it changes, the package is rejected.
- Examples: recipient name, version, record ID, packet header.
- It is written into the tag **with its length**, so the boundary is not
  ambiguous.

## AEAD algorithms

| | AES-GCM | ChaCha20-Poly1305 |
|---|---|---|
| Key | 16 / 24 / 32 bytes | 32 bytes |
| Nonce | 12 bytes | 12 bytes |
| Tag | 16 bytes | 16 bytes |
| Strength | Very fast with hardware support | Fast even without hardware support |
| Nonce reuse | Breaks confidentiality and authentication | Breaks confidentiality and authentication |
