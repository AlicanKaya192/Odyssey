## Formulas

- A random password: **entropy = length × log2(alphabet)** bits.
- Random words: **entropy = number of words × log2(list length)**; with a
  7776-word list, 12.92 bits per word.
- Average number of tries: **2^(bits − 1)**; time = tries / speed.

## Alphabets

| Alphabet | Number of characters | Bits per character |
|---|---|---|
| Digits | 10 | 3.32 |
| Lower-case letters | 26 | 4.70 |
| Letters and digits | 62 | 5.95 |
| Printable ASCII | 94 | 6.55 |

## Kinds of attack

| Attack | What it does | Defence |
|---|---|---|
| Online guessing | Tries on the login page | Limit on tries, waiting, MFA |
| Offline guessing | Tries stolen hashes on its own machine | A slow hash function, salt (Storing Passwords) |
| Dictionary attack | Tries real passwords and patterns | Checking against a list of leaked passwords |
| Credential stuffing | Tries what leaked from another site | A separate password everywhere, MFA |

## Python

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(16))
token = secrets.token_urlsafe(16)
```

- `secrets.choice`, `secrets.token_urlsafe`, `secrets.token_hex`: secure.
- `random.choice`, `random.randint`: predictable; **not used** for
  passwords, tokens or verification codes.

## The rule (today's guidelines)

- Length first; at least 8, preferably 12 or more; allow at least 64
  characters.
- Reject leaked and common passwords.
- No required character types and no regular changes; change only after a
  leak.
- Allow pasting and password managers.
