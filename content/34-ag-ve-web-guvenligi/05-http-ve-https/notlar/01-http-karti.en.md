## The parts of a request

| Part | Example |
|---|---|
| Request line | `POST /login HTTP/1.1` |
| Headers | `Host: shop.example.com`, `Cookie: session=...` |
| Empty line | `\r\n` |
| Body | `user=ada&password=...` |

## Methods

| Method | Job | Does it change state? |
|---|---|---|
| `GET` | Read | No (it must not) |
| `POST` | Send, create | Yes |
| `PUT` / `PATCH` | Change | Yes |
| `DELETE` | Delete | Yes |

## Status codes

| Code | Meaning |
|---|---|
| 1xx | Information |
| 2xx | Success (200 OK, 201 Created) |
| 3xx | Redirect (301 permanent, 302 temporary) |
| 4xx | Client error (400, 401, 403, 404, 429 too many requests) |
| 5xx | Server error (500, 503) |

401 no identity, 403 no permission, 404 does not exist. 404 to hide
existence.

## Security-related headers

| Header | Job |
|---|---|
| `Strict-Transport-Security` | HSTS: never try plain HTTP |
| `Set-Cookie` | Set a cookie (the Sessions and Cookies section) |
| `Content-Security-Policy` | Which scripts may run (CORS and Security Headers) |
| `Location` | The target of a redirect |
| `Server` | The server software; no version is written |

## HTTPS

- HTTPS = HTTP + TLS: **confidentiality, integrity, server identity**.
- It does **not say** the site is trustworthy; the domain name is still
  visible.
- HSTS: `max-age=31536000; includeSubDomains` (one year = 31536000
  seconds).
- Every resource on the page is `https://` (no mixed content).
