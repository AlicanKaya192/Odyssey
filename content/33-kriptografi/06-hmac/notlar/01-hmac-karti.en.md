## What does a MAC provide?

| Question | Answer |
|---|---|
| Has the message changed? | Integrity |
| Was it sent by someone who knows the key? | Authenticity |
| Proof to a third party? | **No** (a signature for that) |

## Python patterns

- Tag: `hmac.new(key, message, hashlib.sha256).hexdigest()`.
- The key and message must be **bytes** (`b"..."` or `.encode()`).
- Verification: recompute the expected tag, `hmac.compare_digest`.
- `hmac.compare_digest(a, b)` is constant-time: it does not give away timing.
- `==` stops at the first differing byte; **never** for comparing a tag, a
  password or a token.

## Rules

- **Do not write** `sha256(key + message)`: open to length extension. Use
  the `hmac` module.
- With an authenticated message, **check the tag first, then use the
  content.**
- The same key is kept separate for encryption and the MAC (the
  Authenticated Encryption section); a single key is split into two by
  deriving separate ones.

## HMAC and a signature

| | HMAC | Digital signature |
|---|---|---|
| Key | Shared (symmetric) | Public + private (asymmetric) |
| Speed | Fast | Slow |
| Who can produce it? | Anyone who knows the key | Only the private-key owner |
| Non-repudiation | No | Yes |
