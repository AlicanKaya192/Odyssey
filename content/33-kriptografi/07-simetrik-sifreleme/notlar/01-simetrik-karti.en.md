## Two kinds

| | Stream cipher | Block cipher |
|---|---|---|
| How | XOR with a keystream | Mixing in fixed blocks |
| Padding | None | Needed (PKCS#7) |
| Example | ChaCha20 | AES |
| Origin | The one-time pad | Substitution + transposition |

## Nonce / IV

- Lets the same key be used for many messages.
- Must be **unique**; need not be secret.
- **Never** used twice with the same key (else the key-reuse mistake).
- Sent in the clear next to the ciphertext.

## PKCS#7 padding

- As many bytes as are missing are added, each equal to that number.
- Even a message of exactly one block length gets **a whole new block**.
- When decrypting, the last byte says the padding length: `data[:-data[-1]]`.

## AES

- Key 128 / 192 / 256 bits; block always 128 bits (16 bytes).
- **Not** in the standard library; used through a library, in an
  authenticated mode (AES-GCM).
- Inside: substitution + transposition, many rounds.

## Rules

- Do not write your own symmetric cipher.
- Encryption alone does not give integrity; use authenticated encryption.
- The key is at least 128 bits, random.
