## Ciphers in one line

| Cipher | Kind | Key | Number of keys | Why is it broken? |
|---|---|---|---|---|
| Caesar | Substitution | Shift | 26 | Brute force |
| ROT13 | Substitution | None (13) | 1 | It has no key |
| Atbash | Substitution | None | 1 | It has no key |
| Substitution | Substitution | An ordering of 26 letters | 26! ≈ 2⁸⁸ | Letter frequency |
| Vigenère | Polyalphabetic substitution | A keyword | 26ᵏ | The key repeats |
| Rail fence | Transposition | Number of rows | Few | Frequencies stay the same |

## Python patterns

- A letter's position in the alphabet: `ord(ch) - ord("a")`.
- Back to a letter: `chr(position % 26 + ord("a"))`.
- Keeping upper and lower case: `base = ord("A") if ch.isupper() else ord("a")`.
- Leave non-letters as they are: `if ch.isalpha() and ch.isascii():`.
- Substitution with a table: `str.maketrans(plain, key)` and `text.translate(table)`.
- In Vigenère the key position only moves on letters.

## To remember

- Decrypting = shifting the other way (`-shift`).
- A large key space alone is not security.
- Substitution → confusion, transposition → diffusion.
