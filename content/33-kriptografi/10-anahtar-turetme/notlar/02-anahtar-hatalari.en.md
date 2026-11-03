Most key derivation mistakes look like they "work"; encryption and
decryption both happen. The problem only shows when someone tries to guess
the password, or when two keys turn out to be the same.

| Mistake | Why it is a problem | The right way |
|---|---|---|
| Using the password directly as the key | The length is wrong, it is not random | PBKDF2 / scrypt / Argon2id |
| Turning the password into a key with one `sha256` | Guessing is very fast | A slow, salted KDF |
| No salt, or the same salt for everyone | The same password gives the same key | A random salt per record |
| Thinking the salt is secret and not storing it | The key cannot be derived again, the data is lost | The salt is stored in the clear next to the data |
| Keeping the iteration count small | No slowness is left | Follow current advice; raise it over time |
| Not writing the parameters into the record | The iteration count cannot be raised later | KDF name and parameters in the record |
| The same derived key for encryption and the MAC | The two operations can weaken each other | HKDF with different `info` labels |
| Giving a password directly to HKDF | HKDF is fast and does not slow guessing | A slow KDF first, then HKDF |
| Writing the derived key to disk | The password's protection is wasted | The key is derived again every time |

## Raising the iteration count

If the iteration count is written in the record, the next time the user
logs in with the right password the key (or the password hash) can be
computed again with a new, higher count and stored. With a record that
does not hold its parameters this is not possible. That is why the record
format in the Storing Passwords section (`algorithm$iterations$salt$hash`)
carries the parameter too.
