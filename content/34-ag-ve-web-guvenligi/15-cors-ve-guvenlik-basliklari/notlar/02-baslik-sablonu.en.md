Values that can be used as a starting point for a new site. Each site
narrows or widens them to its own needs; CSP in particular is written for
the sources the site really loads.

## Suggested values

| Header | Value |
|---|---|
| `Content-Security-Policy` | `default-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `X-Frame-Options` | `DENY` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |

## What the values mean

- **`max-age=31536000`:** one year (in seconds). `includeSubDomains`
  covers every subdomain too; first check that each subdomain is ready for
  HTTPS.
- **`strict-origin-when-cross-origin`:** the full address within the same
  site, only the origin (`https://shop.example`) to another site, nothing
  from HTTPS to HTTP.
- **`frame-ancestors 'none'` and `DENY`:** the page is shown in no frame.
  To allow your own site's frame, `'self'` and `SAMEORIGIN`.
- **`Permissions-Policy`:** turns off browser features the page does not
  use; even if a script slips into the page, it cannot reach the camera.

## Checking

- Header names are compared case-insensitively.
- Headers are sent with **every** response, error pages included.
- CSP is first tried with `Content-Security-Policy-Report-Only`: the
  browser does not block, it only reports the violation.
- Headers are a second layer: escaping, parameterised queries and CSRF
  tokens stay in place.
