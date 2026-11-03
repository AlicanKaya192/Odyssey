## A correctly set session cookie

```text
Set-Cookie: session=<43 characters>; Path=/; Max-Age=3600;
            Secure; HttpOnly; SameSite=Lax
```

## Attributes

| Attribute | Against what? | On a session cookie |
|---|---|---|
| `Secure` | Being read on the way (plain HTTP) | On |
| `HttpOnly` | A script on the page reading it (XSS) | On |
| `SameSite=Lax` | Requests started from another site (CSRF) | On (`Strict` is stricter) |
| `Max-Age` | The cookie living forever | Short |
| `Domain` | Going to too many subdomains | Not written (only its own host) |

`SameSite=None` is accepted only together with `Secure`, and is for cookies
that really need to be used from other sites.

## The session ID

- `secrets.token_urlsafe(32)`: 256 bits, 43 characters.
- **Not** made from a counter, the time, the user name or `random`.
- Not carried in the URL (it ends up in history, logs, `Referer`).
- Not written into logs.

## Life cycle

| Moment | What to do |
|---|---|
| Login | Make a new ID, delete the old one (against fixation) |
| Privilege change | Renew the ID |
| Every request | Check the idle and absolute timeouts |
| Logout | Delete the record on the server, delete the cookie |
| Password change | Close all other sessions |

## Signed cookies

- If state is kept in the cookie, it is signed with HMAC and verified
  with `compare_digest`.
- A signature **does not hide**; secret information is not written into a
  cookie.
- An expiry time is put inside it; the server cannot recall it on its own.
