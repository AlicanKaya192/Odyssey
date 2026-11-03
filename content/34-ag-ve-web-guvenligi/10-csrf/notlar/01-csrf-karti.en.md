## CSRF at a glance

| Question | Answer |
|---|---|
| Why does it happen? | The browser attaches the cookie without looking at where the request started |
| What does the attacker do? | Gets an **action** done in the user's name |
| Can they read the response? | No (the same-origin policy) |
| Do they steal the cookie? | No; the browser attaches it itself |
| Which requests? | Those that change state: `POST`, `PUT`, `PATCH`, `DELETE` |

## Defences

| Defence | How? | Note |
|---|---|---|
| CSRF token | Make with `secrets`, tie to the session, send in the form, `compare_digest` | The main defence |
| Double-submit cookie | The token in both a cookie and the form; the two are compared | Without storing on the server |
| `SameSite=Lax` / `Strict` | No cookie on a `POST` from another site | Write it explicitly; a second layer |
| `GET` changes no state | Work that changes state with `POST` | `Lax` attaches the cookie to a top-level `GET` |
| Origin check | Is `Origin` in the allow list? | The rule for a missing header is set in advance |
| Re-authentication | Password or MFA for important actions | Another site does not know the password |

## The SameSite decision (request from another site)

| Attribute | Top-level `GET` | Hidden-form `POST` |
|---|---|---|
| `Strict` | No cookie | No cookie |
| `Lax` | Cookie | No cookie |
| `None` (+ `Secure`) | Cookie | Cookie |

## Rules

- The token stays only inside the page; it is not carried in the address
  (`?csrf=...`).
- The token differs for each session; when the session is renewed, the
  token is renewed too.
- An XSS hole defeats all CSRF defences.
- CORS is not a CSRF defence (the CORS and Security Headers section).
