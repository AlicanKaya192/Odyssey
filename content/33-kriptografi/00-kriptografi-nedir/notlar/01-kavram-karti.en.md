## Terms

| Term | One line |
|---|---|
| Plaintext | The message to protect |
| Ciphertext | The output of encryption |
| Key | The only secret part |
| Encoding | No key, anyone reverses it (Base64, hex) |
| Hash | A fixed-length fingerprint, not reversible |
| Symmetric | Encrypt and decrypt with the same key |
| Asymmetric | Encrypt with the public key, decrypt with the private key |
| Brute force | Trying every key one by one |

## Kerckhoffs's principle

The algorithm may be public; security rests only on the secrecy of the key.

## Key length

- `n` bits = `2ⁿ` keys; every extra bit doubles brute force.
- At 10¹² guesses per second 40 bits takes about 1 second, 56 bits about
  20 hours, 128 bits more than 10¹⁹ years.
- Today's lower limit for a symmetric key is 128 bits.

## To remember

- Base64 is not encryption.
- Cryptography does not provide availability; if the key is lost, so is the
  data.
- In a real application, do not write your own algorithm or protocol.
