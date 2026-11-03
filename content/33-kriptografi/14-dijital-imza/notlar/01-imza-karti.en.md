## Signing and verifying

| Step | Who | Operation |
|---|---|---|
| Hash | The signer | `h = sha256(message)` |
| Sign | The signer (private key) | `s = sign(h, private)` |
| Send | | `message`, `s` |
| Verify | Anyone (public key) | `verify(s, hash(message), public)` |

In toy RSA: `s = pow(h, d, n)`, verification `pow(s, e, n) == h`.

## What it says

- **Integrity:** the message has not changed since it was signed.
- **Source:** the owner of this private key signed it.
- **Non-repudiation:** the signer cannot later say "it was not me".

It does **not** provide confidentiality: a signed message stays in the
clear. If confidentiality is also needed, the message is encrypted
separately.

## Algorithms

| | RSA-PSS | ECDSA | Ed25519 |
|---|---|---|---|
| Key | 2048+ bits | 256 bits | 256 bits |
| Random number per signature | In the padding | **Required, never repeated** | Not needed (deterministic) |
| Note | The textbook RSA signature is not used | A repeated number reveals the private key | Often chosen in new systems |

## The verifier's rules

1. Signature first, then content: if the signature does not match, no field
   of the message is used.
2. Verify with the right public key: the key comes from a certificate or an
   already trusted path, not from inside the message.
3. If the signed content has a version or a date, check it too: to stop an
   old but validly signed version from being installed again.
