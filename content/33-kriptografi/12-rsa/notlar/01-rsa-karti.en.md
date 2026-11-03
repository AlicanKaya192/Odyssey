## Key generation

| Step | Formula | Toy example |
|---|---|---|
| Two primes | `p`, `q` | 61, 53 |
| Modulus | `n = p * q` | 3233 |
| `phi` | `(p - 1) * (q - 1)` | 3120 |
| Public exponent | `gcd(e, phi) == 1` | 17 (65537 in practice) |
| Private exponent | `d = pow(e, -1, phi)` | 2753 |

- **Public key:** `(e, n)`. Given to everyone.
- **Private key:** `(d, n)`. `p`, `q` and `phi` are secret too.

## Encryption and decryption

| Operation | Formula | Example |
|---|---|---|
| Encrypt | `c = pow(m, e, n)` | `pow(65, 17, 3233) = 2790` |
| Decrypt | `m = pow(c, d, n)` | `pow(2790, 2753, 3233) = 65` |

- `m < n` is required; a large message is not encrypted directly.
- Text → number: `int.from_bytes(data, "big")`; back: `number.to_bytes(length, "big")`.

## Why it is secure

Finding `d` from `n` needs `phi`, and that needs `p` and `q`. There is no
known fast way to split a big `n` into its primes. Security depends
entirely on the **size** of `n`.

## The problem with textbook RSA

- It is deterministic: the same message → the same ciphertext.
- If the possible messages are few, anyone can try them with the public key
  and compare.
- The fix: random padding before encrypting, **OAEP**.
