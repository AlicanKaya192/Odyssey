Using symmetric encryption correctly depends less on choosing the
algorithm than on how you use it. A checklist bringing together the lessons
of this section and the earlier ones:

## The key

- At least 128 bits, truly random (`secrets`/`os.urandom`; not `random`).
- Not written into code; read from configuration or a secrets vault.
- The encryption key and the MAC key are separate; derived separately from
  one master secret (the Key Derivation section).
- Do not use a password directly as a key; a key is derived from a password
  with a KDF.

## The nonce / IV

- Unique for every message. The safest way is to generate it at random or
  keep a safe counter.
- Never repeated with the same key.
- Not secret; stored/sent next to the ciphertext.

## Confidentiality is not enough: integrity too

- Encryption alone does not stop the message being changed (the bit
  flipping in the XOR section).
- The fix: encryption + a MAC, or **authenticated encryption** that does
  both (AES-GCM, ChaCha20-Poly1305). The Authenticated Encryption section.
- The receiver verifies the tag **first**, then decrypts.

## Use a library

- AES and modern stream ciphers are not in the standard library; the
  high-level, authenticated function of a well-tested library is used.
- Instead of joining modes, padding and the nonce by hand, a single
  "encrypt/decrypt" call is preferred; the less detail, the fewer mistakes.
- Everything we write in this note and the lesson is for **learning**, not
  for use in production.
