## The parts of the handshake

| Message | Contains | Which section |
|---|---|---|
| ClientHello | Versions, cipher suites, key share | Diffie-Hellman and Elliptic Curves |
| ServerHello | Chosen version and suite, key share | Diffie-Hellman and Elliptic Curves |
| (the keys) | HKDF; transcript hash in the label; separate per direction | Key Derivation |
| Certificate | The server's certificate chain | Certificates and PKI |
| CertificateVerify | The server's signature over the transcript hash | Digital Signatures |
| Finished | HMAC over the hash of the whole handshake | Message Authentication: HMAC |
| Application data | Records encrypted with AEAD | Authenticated Encryption |

## The transcript hash

- Every message that goes back and forth is added to one hash **in order**.
- It is used in key derivation, in the signature and in Finished.
- A message changed on the way splits the two sides' hashes; Finished does
  not match.

## Settings

| Topic | The right way |
|---|---|
| Version | TLS 1.3; TLS 1.2 if needed |
| Turned off | SSL 3.0, TLS 1.0, TLS 1.1 |
| TLS 1.3 suites | `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256` |
| TLS 1.2 suites | Only ECDHE + AEAD (GCM or ChaCha20-Poly1305) |
| Certificate verification | Always on |
| HSTS | On, so that `https` stays |

## Choosing the version and suite

The client lists what it supports; the server picks, **from its own
preference list**, the first one the client also supports. If there is no
common option, the handshake ends with an error; there is no "falling back"
to a weak option.
