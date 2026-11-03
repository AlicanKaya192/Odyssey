## Four properties

| Property | Meaning |
|---|---|
| Deterministic | Same input → same digest |
| One-way | Cannot go from digest to input |
| Collision resistant | No two inputs with the same digest can be found |
| Avalanche | Changing one bit changes half the digest |

## Algorithms

| Name | Bits | Status |
|---|---|---|
| MD5 | 128 | Broken |
| SHA-1 | 160 | Broken |
| SHA-256 | 256 | Secure (SHA-2) |
| SHA-512 | 512 | Secure (SHA-2) |
| SHA-3 (sha3_256) | 256 | Secure |
| BLAKE2b | 512 | Secure, fast |

## Python patterns

- Hex digest: `hashlib.sha256(data).hexdigest()`.
- Raw bytes: `hashlib.sha256(data).digest()`.
- By name: `hashlib.new("sha256")`, size `.digest_size`.
- Text to bytes: `"text".encode()`; a hash always works on bytes.
- Bit difference: `bin(int.from_bytes(a,"big") ^ int.from_bytes(b,"big")).count("1")`.

## Use and misuse

| Job | Right | Wrong |
|---|---|---|
| File integrity | SHA-256 | MD5 (broken) |
| Storing a password | Slow salted hash | Plain SHA-256 |
| Proof of sender + integrity | HMAC | Plain hash |
| Deduplication | Any hash | — |

## To remember

- Birthday bound: a collision in `2^(n/2)` tries; 256 bits is secure.
- A plain hash does not stop a deliberate change, it only catches
  accidental corruption.
