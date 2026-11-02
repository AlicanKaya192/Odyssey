When choosing a password storage algorithm, three questions matter: is the
salt built in, how slow can it be set to be, and does it spend memory?

| Algorithm | Setting | Spends memory? | Note |
|---|---|---|---|
| **PBKDF2** | Iteration count | No | In the standard library (`hashlib.pbkdf2_hmac`); common and approved |
| **bcrypt** | Cost factor | A little | Used for many years; looks at the first 72 bytes of the password |
| **scrypt** | `n`, `r`, `p` | Yes | Comes with `hashlib.scrypt` |
| **Argon2id** | Time, memory, parallelism | Yes | Usually the first recommendation for new systems |

## Why memory?

Password guessing uses hardware with very many simple cores. Each core
makes its own tries. If the algorithm needs some memory for every try, the
number of cores runs into memory limits; the attack gets expensive.
PBKDF2 only spends time, so its iteration count is kept high.

## Choosing the parameters

- Decide how long the server can afford for one login (for example a few
  hundred milliseconds) and tune the parameters to that time.
- Recommended values go up as hardware gets faster. For the current values
  see OWASP's password storage guide.
- Because the parameters are written in every record, changing them does
  not break old records.

## Upgrading old records

The user's password is only available in the clear at login. So:

1. When a login is verified, look at the record's algorithm and
   parameters.
2. If they are old, hash the password again with the new algorithm and
   parameters.
3. Write the new record in place of the old one.

If weak records such as plain SHA-256 are left for users who have not
logged in for a long time, wrapping the old hash inside the new algorithm
(a hash of the hash) is a way to migrate; then all of them are protected
without waiting for a login.

## Do not

- Do not invent your own "clever" hash scheme (SHA-256 twice, writing it
  backwards).
- Do not use the same salt for every user.
- Do not write passwords into logs or error messages.
- Do not cut the password length too short; a slow hash takes the same time
  for a long password (except for bcrypt's 72-byte limit).
