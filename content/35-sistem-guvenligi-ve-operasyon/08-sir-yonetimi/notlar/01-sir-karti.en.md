## A secret's life cycle

| Step | Right way | Wrong way |
|---|---|---|
| Generate | `secrets.token_urlsafe(32)` | `random`, a word someone made up |
| Store | A secrets vault, encrypted | In code, in the repository, in a plain text file |
| Give to the program | An environment variable or the vault | A constant inside the code |
| Use | Only where needed, in memory | Writing it to a log or an error message |
| Rotate | Regularly; at once if leaked | "It works, do not touch it" |
| Revoke | The old value is made invalid | Only deleting it |

## Python patterns

- Stop if missing: `if not env.get(name): raise RuntimeError(...)`.
- Hide in a log: `re.sub(r"(password|token)=\S+", r"\1=***", line)`.
- Show the last characters: `"*" * 4 + value[-4:]`.
- Shannon entropy: `-sum(p * math.log2(p) for p in ratios)`.
- Age: `(today - created).days > max_days`.

## Entropy scale

| Text | Bits per character |
|---|---|
| `aaaaaaaa` | 0.00 |
| `password` | 2.75 |
| `q8Zr2LxP0vT7mWk9` | 4.00 |

A repeat of a single kind of character carries 0 bits; 16 different
characters can carry at most 4 bits.

## Keep in mind

- A secret deleted from the repository stays in the history; it counts as
  leaked and is rotated.
- An error message holds the secret's name, not its value.
- Entropy scanning is an estimate: it gives false alarms and also misses.
- Secret files such as `.env` stay out of the repository and have
  permission `600`.
