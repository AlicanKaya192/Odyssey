An IV and a nonce do the same job: they keep two messages encrypted with
the same key from looking alike. The rules change a little with the mode.

## Common rules

- **It is not secret.** It is put in front of the ciphertext and stored or
  sent with it. The receiver needs it to decrypt.
- **It is not repeated with the same key.** If it is, the same message gives
  the same ciphertext and the mode falls back to ECB's problem (worse in
  CTR: the key-reuse mistake).
- **It is not hard-coded.** A line such as `iv = b"0000000000000000"` means
  the same IV for every message.

## The IV in CBC

- Being unique is not enough; it must also be **unpredictable**.
- The right way: `secrets.token_bytes(16)` (or `os.urandom(16)`) for every
  message.
- The `random` module is not used: it is not made for values that must be
  secret or unpredictable.

## The nonce in CTR and GCM

- It may be predictable but must be **strictly unique**.
- Two safe ways: a random nonce for every message, or a counter that is
  stored permanently and never rewinds.
- If a counter is used, it must not start again from zero when the program
  restarts.

## Quick check

| Question | Right answer |
|---|---|
| Do I need to store the IV? | Yes, next to the ciphertext |
| Do I need to hide the IV? | No |
| Can I reuse the same IV? | No, never with the same key |
| How do I make an IV? | `secrets.token_bytes(16)` |
| Does ECB have an IV? | No, and that is its problem |
