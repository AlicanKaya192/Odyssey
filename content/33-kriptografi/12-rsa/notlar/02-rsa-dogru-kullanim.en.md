The mathematics of RSA is short, but using it correctly depends on many
details. This list is what to check when choosing a library and reading its
settings.

## Checklist

| Topic | The right way | The wrong way |
|---|---|---|
| Key size | At least 2048 bits; 3072 for a long-lived key | 512 or 1024 bits |
| Public exponent | 65537 | A very small exponent (e.g. 3) with no padding |
| Encryption padding | OAEP | No padding (textbook) RSA |
| Signature padding | PSS | An unpadded signature |
| Large data | Hybrid encryption: RSA only carries the symmetric key | Encrypting the data piece by piece with RSA |
| Key generation | A well-tested library, secure randomness | Writing your own prime generator |
| Private key | In an encrypted file or a key vault | In the code, in the repository |
| Same key pair | Separate pairs for encryption and signing | Using one pair for everything |

## Hybrid encryption steps

1. Make a random symmetric key (`secrets.token_bytes(32)`).
2. Encrypt the data with this key using authenticated encryption such as
   AES-GCM.
3. Encrypt the symmetric key with the receiver's **public** RSA key, using
   OAEP.
4. Send both together. The receiver decrypts the symmetric key with the
   private key, and the data with that.

## What is replacing RSA

New systems mostly prefer elliptic-curve Diffie-Hellman (X25519) for key
exchange and Ed25519 or ECDSA for signatures: the keys are much shorter and
the operations faster. RSA is still common in certificates and older
systems.
