## Network

| Topic | Remember |
|---|---|
| Private ranges | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`; loopback `127.0.0.0/8` |
| CIDR | `/24` → 256 addresses; each extra bit halves it |
| TCP / UDP | Reliable, with a handshake / fast, no guarantee |
| Firewall | The first matching rule; default deny at the end; egress filtering |
| Segmentation | An allow list between zones; DMZ; zero trust |
| DNS | Cached for the TTL; DNSSEC integrity, DoT/DoH privacy |
| HTTPS | Confidentiality + integrity + server identity; HSTS `max-age=31536000` |

## Web: attack → defence

| Attack | First defence | Extra layer |
|---|---|---|
| SQL injection | Parameterised query (`?`) | An allow list for names, a least-privileged database user |
| XSS | Output encoding by context (`html.escape`) | CSP, `HttpOnly` |
| CSRF | A session-bound token + `compare_digest` | `SameSite=Lax`, an `Origin` check |
| SSRF | An allow list on the parsed address | Refusing internal addresses on the IP, egress filtering |
| Broken access control | An ownership check for every object | Hiding existence with `404` |
| Credential stuffing | Growing delays, MFA | Monitoring per source |
| Path traversal | `normpath` + `startswith(BASE + "/")` | A random file name |
| Command injection | An argument list | `shlex.quote` |
| Mass assignment | A field allow list | Reporting the rejected with `422` |
| Clickjacking | `frame-ancestors 'none'` | `X-Frame-Options: DENY` |

## Cookies and headers

| Name | Value |
|---|---|
| Session cookie | `Secure; HttpOnly; SameSite=Lax` |
| CORS | An origin from the allow list + `Vary: Origin` |
| Type | `X-Content-Type-Options: nosniff` |
| Referrer | `Referrer-Policy: strict-origin-when-cross-origin` |

## Python tools

| Job | Tool |
|---|---|
| Addresses and networks | `ipaddress.ip_address`, `ip_network`, `in` |
| Parsing an address | `urllib.parse.urlsplit` (`.scheme`, `.hostname`, `.port`) |
| Form | `re.fullmatch` |
| A random value | `secrets.token_urlsafe(32)` |
| Comparing | `hmac.compare_digest` |
| Signing | `hmac.new(secret, message, hashlib.sha256)` |
| Encoding | `html.escape`, `urllib.parse.quote(s, safe="")`, `json.dumps` |
