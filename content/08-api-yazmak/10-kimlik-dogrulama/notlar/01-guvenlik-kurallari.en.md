The dos and don'ts of authentication, in one list.

## Do

- Store passwords with a **salted, slow** hash (`pbkdf2_hmac`, `bcrypt`,
  `argon2`). A separate salt for every user.
- Compare hashes with `hmac.compare_digest`.
- Generate tokens and keys with the `secrets` module (`token_hex`,
  `token_urlsafe`).
- Send/read keys and tokens in **headers**.
- At login, answer "no such user" and "wrong password" with the **same**
  message (`"Wrong username or password"`): separate messages reveal which
  usernames exist.
- HTTPS on a real server.

## Don't

| Don't | Why? |
|---|---|
| Store passwords as plain text | If the database leaks, they're all gone |
| `hashlib.sha256(password)`, one round, no salt | Fast: millions of guesses take seconds |
| A token from `random.randint` | `random` is predictable |
| Send a key in the query | It gets written to logs and history |
| Write a password or token into an answer/log | It leaks |
| Compare hashes with `==` | The time difference gives hints |

## 401 or 403?

| Situation | Code |
|---|---|
| No header | `401` |
| Key/token not recognised | `401` |
| Wrong password | `401` |
| The user is known but not allowed to do this | `403` |

Adding a `WWW-Authenticate` header to a `401` is an HTTP rule; `HTTPBearer`
does it by itself.
