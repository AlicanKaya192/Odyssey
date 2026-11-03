**Diffie-Hellman + key derivation.** `derive` is ready (a 32-byte key from
the shared secret with HMAC). `session_key(p, g, a, b)` should compute both
sides' session keys and return `[equal, ada_key]`. Each side computes the
shared secret from **the other side's** public value. In the starter code
Ada uses her own public value and the keys do not match.

**Expected output:**

```
True
32 bytes
```
