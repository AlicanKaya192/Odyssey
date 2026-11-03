An API key and a request signature answer two separate questions: the
key "who", the signature "unchanged and fresh".

## API keys

- **Generating:** `secrets.token_urlsafe(32)`; no guessable value (user
  name, date, sequence number).
- **Prefix:** a prefix such as `shop_live_...` shows what the key belongs
  to and makes searching for a leaked key (in a code repository, in a log)
  easier.
- **Storing:** only its hash on the server (`sha256`); the key is shown to
  the user once.
- **Sending:** in a header (`Authorization`), not in the address.
- **Comparing:** `hmac.compare_digest`.
- **Scope:** each key allows only the jobs it needs (read only, say); the
  principle of least privilege.
- **Renewing:** a key has a lifetime; a new one is issued and the old one
  is closed after a while. A leaked key is revoked at once.

## Request signatures

The signed text contains all the important parts of the request:

| Part | Why |
|---|---|
| Time (`ts`) | To refuse an old request |
| Method (`POST`) | So a `GET` signature is not used for `DELETE` |
| Path (`/transfer`) | So it is not moved to another endpoint |
| Body | So the amount and recipient do not change |
| Nonce | So it is not used a second time inside the window |

- The server **recomputes** the signature itself and compares with
  `hmac.compare_digest`.
- Time first, then the signature; both are needed together.
- A small window (a few minutes) is left for clock differences; nonces are
  remembered for as long as that window.
- On both sides the secret goes into secret management, not into the code
  repository.
