## Two generators

| | `random` | `secrets`, `os.urandom` |
|---|---|---|
| Kind | Pseudo-random (PRNG) | Cryptographic (CSPRNG) |
| Source | Seed + formula | The operating system's noise source |
| Same seed | Same sequence | No seed |
| Use | Simulations, games, sampling | Keys, nonces, salts, tokens, passwords |

## `secrets` functions

| Call | Gives | Example job |
|---|---|---|
| `token_bytes(n)` | `n` random bytes | Key, nonce, salt |
| `token_hex(n)` | `n` bytes, `2n` hex characters | Token, API key |
| `token_urlsafe(n)` | `n` bytes, Base64 (safe in links) | Password reset link |
| `randbelow(n)` | A whole number from `0` to `n - 1` | Verification code |
| `choice(seq)` | One item from the sequence | Password character |

`os.urandom(n)` also gives `n` random bytes; it is the same source as
`token_bytes`.

## Sizes

| Value | Bytes | Bits |
|---|---|---|
| AES-256 key | 32 | 256 |
| AES-GCM nonce | 12 | 96 |
| Salt | 16 | 128 |
| Long-lived token | at least 16 | at least 128 |

## Entropy

- `n` randomly chosen characters, an alphabet of `a` letters: `n × log2(a)`
  bits.
- Writing a letter twice in the alphabet does not add any possibilities:
  `a` is the number of **different** characters.
- The length needed for 128 bits: `math.ceil(128 / math.log2(a))`.

| Alphabet | Bits per character | For 128 bits |
|---|---|---|
| 10 digits | 3.32 | 39 characters |
| 16 hex | 4 | 32 characters |
| 62 letters and digits | 5.95 | 22 characters |
| 64 Base64 | 6 | 22 characters |

## Modulo bias

- `byte % 100`: results 0–55 come out 3 times in 256, results 56–99 twice.
- The right way: throw away anything at or above `256 - 256 % n` and draw
  again.
- In Python `secrets.randbelow(n)` does this; do not write it by hand.
