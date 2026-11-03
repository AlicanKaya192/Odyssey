# Overall Review

This module first looked at how a packet travels across the network, then
at the web applications that sit on that path: layers and addresses,
network attacks, firewalls and segmentation, DNS, HTTPS, sessions, the
common weaknesses OWASP lists and their defences. This section looks at
them all together; at the end there are 40 mixed questions and five
exercises that combine several sections.

## A map of the module

| Topic | Main idea |
|---|---|
| **Network layers** | Application, transport, network, link; encapsulation; CIDR and private ranges; every open port is attack surface. |
| **Network attacks** | Protocols do not verify the other side: eavesdropping, man in the middle, ARP, spoofed source addresses, SYN floods, replay. |
| **Firewalls** | The first matching rule from top to bottom, default deny, stateful filtering, egress filtering; a WAF is an extra layer. |
| **VPNs and segmentation** | A VPN protects part of the path; zones and allow lists narrow lateral movement; zero trust. |
| **DNS security** | Cache poisoning, DNSSEC signatures, encrypted DNS; dangling records. |
| **HTTP and HTTPS** | Every part of the request is in the user's hands; 401/403/404; TLS gives confidentiality, integrity, server identity; HSTS. |
| **Sessions and cookies** | Ids from `secrets`; Secure, HttpOnly, SameSite; renewal at login; time limits; signed cookies. |
| **OWASP Top 10** | Access control, injection, configuration, components, integrity, logging; the list is a starting point. |
| **SQL injection** | Parameterised queries; an allow list for names; `LIKE` escaping; second order. |
| **XSS** | Output encoding by context; scheme checks; auto-escaping templates; CSP. |
| **CSRF** | A session-bound token, SameSite, origin checks; `GET` does not change state. |
| **SSRF** | An allow list on the parsed address; refusing internal addresses on the IP; redirects. |
| **Authentication failures** | The same message, growing delays, one-time reset codes, length and a common-password list. |
| **Input validation and encoding** | Canonical form first, `fullmatch`, an allow list; path traversal; argument lists; validation does not replace encoding. |
| **Secure APIs** | Ownership for every object; field allow lists in and out; a bucket limit; key hashes; HMAC signatures. |
| **CORS and headers** | Origin = scheme + name + port; CORS with an allow list and `Vary: Origin`; preflight; CSP, HSTS, `nosniff`, frame blocking. |

## The path of a request

When a web request reaches the server, most of the module's defences come
into play in order:

<figure class="fig"><div class="flow">
  <span class="node">Session</span><span class="arrow">→</span>
  <span class="node acc">Origin + CSRF</span><span class="arrow">→</span>
  <span class="node acc">Ownership</span><span class="arrow">→</span>
  <span class="node">Parameterised query</span><span class="arrow">→</span>
  <span class="node ok">Encoded response</span>
</div><figcaption>Who it is, where the request came from, whose the object is, data not being code, and output encoded for its context.</figcaption></figure>

The small notes application below does this from start to finish. The
database is in memory, the requests are dictionaries; there is no network
connection:

```python
import hmac
import html
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE notes (id INTEGER, owner TEXT, body TEXT)")
db.executemany(
    "INSERT INTO notes VALUES (?, ?, ?)",
    [(1, "ada", "<b>hi</b>"), (2, "bob", "secret")],
)
SESSIONS = {"s-ada": {"user": "ada", "csrf": "t-123"}}
ALLOWED_ORIGINS = {"https://notes.example"}


def handle(method, note_id, headers, form=None):
    session = SESSIONS.get(headers.get("cookie", ""))
    if session is None:
        return 401, "login required"
    if method == "POST":
        if headers.get("origin") not in ALLOWED_ORIGINS:
            return 403, "bad origin"
        if not hmac.compare_digest(form.get("csrf", ""), session["csrf"]):
            return 403, "bad csrf token"
    row = db.execute(
        "SELECT body FROM notes WHERE id = ? AND owner = ?",
        (note_id, session["user"]),
    ).fetchone()
    if row is None:
        return 404, "not found"
    return 200, "<p>" + html.escape(row[0]) + "</p>"


ada = {"cookie": "s-ada", "origin": "https://notes.example"}
print(handle("GET", 1, ada))
print(handle("GET", 2, ada))
print(handle("GET", 1, {}))
print(handle("POST", 1, {"cookie": "s-ada", "origin": "https://other.example"}, {}))
print(handle("POST", 1, ada, {"csrf": "guess"}))
print(handle("POST", 1, ada, {"csrf": "t-123"}))
```

```text
(200, '<p>&lt;b&gt;hi&lt;/b&gt;</p>')
(404, 'not found')
(401, 'login required')
(403, 'bad origin')
(403, 'bad csrf token')
(200, '<p>&lt;b&gt;hi&lt;/b&gt;</p>')
```

Line by line: the `<b>` inside the note was encoded and will show as text
on the page (XSS). `bob`'s note came back to `ada` with `404`; the note
exists but is not hers (object level authorization, a response that does
not reveal existence). The request without a cookie got `401`. The `POST`
from another origin was turned away before the token was looked at (the
origin check), and so was the one from the right origin with the wrong
token (the CSRF token, a constant-time comparison). Only the last request
got through every gate. The ownership check is done inside the query and
with parameters: whatever `note_id` is, it stays data (SQL injection).

In a real application the session id and the token are generated with
`secrets`, the cookie is sent with `Secure; HttpOnly; SameSite=Lax`, and
security headers are added to the response; here they are short, fixed
values so they are readable.

## Commonly confused pairs

| Pair | Difference |
|---|---|
| Authentication / authorization | "Who are you?" / "Is this object yours, may you do this?" |
| `401` / `403` / `404` | No identity / no permission / not found (or existence hidden) |
| Validation / encoding | Is the data in the expected form / data must not become code where it is written |
| XSS / CSRF | Someone else's code runs on the page / another site sends a request on the user's behalf |
| CSRF / SSRF | The browser is tricked / the server is tricked |
| Same-origin policy / CORS | Blocks reading / the server allowing reading |
| DNSSEC / encrypted DNS | Was the answer changed / who sees the query |
| VPN / HTTPS | Protects part of the path / protects browser to site end to end |
| Allow list / block list | Describes what is valid / counts known bad, always forgets something |
| Stateless / stateful firewall | Judges each packet separately / remembers connections |
| Security header / application fix | A second layer / the real solution |

## Common threads

The sections look at different topics, but the same few ideas kept coming
back:

- **Everything from the user is input:** address, header, cookie, body,
  file name, another API's response.
- **Allow list, default deny:** firewall rules, origins, fields, schemes,
  hosts, file types.
- **Parse, then decide:** an address with `urlsplit`, not as text; a path
  with `normpath`; an IP with `ipaddress`.
- **Keep data and code apart:** parameterised queries, encoding by context,
  argument lists.
- **Secrets are generated with `secrets` and compared with
  `compare_digest`.**
- **Defence in depth:** every layer (segmentation, WAF, CSP, SameSite) is
  there to catch what the one before missed; none of them replaces the
  real fix.

## Summary

- The network is layered; because most protocols do not verify the other
  side, encryption and authentication are needed together.
- At the network layer, firewalls, segmentation and zero trust; at the
  name layer, DNSSEC and encrypted DNS; in transport, TLS and HSTS.
- In a web application, for every request: the session, the origin and
  the CSRF token, the object's ownership, a parameterised query, output
  encoded by context.
- The requests the server sends out (SSRF) and the limits of APIs are
  protected with the same allow-list thinking.
- Headers and browser policies are a second layer; the real defence is in
  the application's own code.
