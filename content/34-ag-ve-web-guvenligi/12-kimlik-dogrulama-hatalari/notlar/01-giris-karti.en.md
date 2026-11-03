## Mistake and defence

| Mistake | Defence |
|---|---|
| Different error messages (user enumeration) | One message; compute a hash for an unknown user too |
| Unlimited attempts (brute force) | Limits per account and per source, increasing delay |
| Credential stuffing | MFA, monitoring per source, a leaked-password list |
| Locking the account completely | Increasing delay (a lock opens the door to denial of service) |
| A predictable reset token | `secrets`, short life, single use, hashed on the server |
| A weak password rule | Minimum length, rejecting known bad passwords |
| Default passwords | Require changing them at installation |
| Skippable MFA | The second step is checked on the server |

## Increasing delay

| Failures | 1 | 2 | 3 | 4 | 5 | 10 | 11 |
|---|---|---|---|---|---|---|---|
| Delay (s) | 0 | 0 | 1 | 2 | 4 | 128 | 256 |

Rule: after 3 failures, `2 ** (failures - 3)` seconds, at most 300.

## The reset token

- `secrets.token_urlsafe(32)`
- On the server `hashlib.sha256(token.encode()).hexdigest()`
- A short life (e.g. 900 seconds), single use (`used`)
- Compared with `hmac.compare_digest`
- After a successful reset, the other sessions are closed

## Messages

| Situation | What the user sees |
|---|---|
| Wrong name or password | "Invalid user name or password" |
| Reset request | "If this address is registered, we sent a link" |
| Too many attempts | "Try again in a while" |
