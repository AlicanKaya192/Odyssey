When reviewing code or taking over a project, ask these questions in
order about its cryptography.

## Code

- [ ] Are secret values made with `secrets`? (No `random`.)
- [ ] Is there a key, password or token written in quotes in the source?
- [ ] Are tag and hash comparisons done with `hmac.compare_digest`?
- [ ] Is there home-made cipher, mode or padding code? (There should not be.)
- [ ] Is decrypted data used before its tag is verified?

## Settings

| Setting | Accept | Reject |
|---|---|---|
| Hash | SHA-256, SHA-384, SHA-512, SHA-3, BLAKE2 | MD5, SHA-1 |
| Symmetric | AES-GCM, ChaCha20-Poly1305 | ECB, CBC/CTR without authentication, DES, RC4 |
| AES key | 128, 192, 256 bits | Shorter |
| RSA key | 2048+ bits, OAEP / PSS | 1024 and below, unpadded |
| Curve | 256+ bits (X25519, P-256, Ed25519) | Shorter |
| Password KDF | Argon2id, scrypt, PBKDF2 (hundreds of thousands of iterations) | A single hash, no salt |
| Nonce / IV | Unique for every message | Fixed, counter resets |
| TLS | 1.3, strong 1.2; verification on | 1.0, 1.1, `verify=False` |

## Key management

- [ ] Are keys in a secret vault or an environment variable?
- [ ] Is there a separate key for each purpose (encryption, MAC, signing)?
- [ ] Is there a plan for rotating (changing) keys?
- [ ] Is it written down what to do with a leaked key?
