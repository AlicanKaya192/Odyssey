## SSRF at a glance

| Question | Answer |
|---|---|
| What happens? | The server sends a request on its own behalf to an address the user gives |
| Why is it dangerous? | The server is inside; it reaches addresses that cannot be reached from outside |
| Which features? | Image fetching, link previews, webhooks, file import |
| Special risk in the cloud | The metadata service in the link-local range (`169.254.0.0/16`) |

## Addresses to refuse

| Kind | `ipaddress` property | Example |
|---|---|---|
| Loopback | `is_loopback` | `127.0.0.1` |
| Private | `is_private` | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` |
| Link-local | `is_link_local` | `169.254.0.0/16` |
| Unspecified | `is_unspecified` | `0.0.0.0` |
| Reserved | `is_reserved` | `240.0.0.0/4` |

## Python patterns

- Parse: `parts = urlsplit(url)`; `parts.scheme`, `parts.hostname`,
  `parts.port`.
- Scheme: `parts.scheme in ("http", "https")`.
- Allow list: `parts.hostname in ALLOWED_HOSTS` (exact equality).
- IP check: resolve the name, `ipaddress.ip_address(...)`, the internal
  address properties.
- An address that cannot be resolved or is invalid: refuse.

## Rules

- An address is not checked with a text search (`startswith`, `in`).
- The check is made **after resolution** on the IP; the connection is
  opened **to the checked IP**.
- Redirects are not followed, or every step is re-checked.
- Egress filtering for the fetch component; no path to the internal
  network or the metadata address.
- The response type, size and timeout are limited; error details are not
  shown.
