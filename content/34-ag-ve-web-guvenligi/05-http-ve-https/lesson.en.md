# HTTP and HTTPS

DNS turned the name into an address, the TCP connection is set up; now the
browser and the server start to talk. The language of the web is **HTTP**
(HyperText Transfer Protocol). All the web attacks in the rest of the
module (session theft, SQL injection, XSS, CSRF) travel inside HTTP
messages; so we first learn to read an HTTP message. Then we move on to
**HTTPS**, which protects the same message on the way. All messages stay as
text in Python; no request is sent.

## An HTTP request

HTTP is a text-based protocol: a request is plain text made of lines. The
first line is the **request line** (method, path, version); then come the
**headers**; after an empty line, the **body**, if there is one. Lines end
with `\r\n`.

```python
raw = (
    "POST /login HTTP/1.1\r\n"
    "Host: shop.example.com\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Cookie: session=abc123\r\n"
    "\r\n"
    "user=ada&password=s3cret"
)

head, body = raw.split("\r\n\r\n", 1)
lines = head.split("\r\n")
method, path, version = lines[0].split(" ")
headers = dict(line.split(": ", 1) for line in lines[1:])
print(method, path, version)
for name, value in headers.items():
    print(f"{name}: {value}")
print("body:", body)
```

```text
POST /login HTTP/1.1
Host: shop.example.com
Content-Type: application/x-www-form-urlencoded
Cookie: session=abc123
body: user=ada&password=s3cret
```

Note four things:

- The **method** says what is wanted. `GET` reads something, `POST` sends
  or creates, `PUT`/`PATCH` change, `DELETE` deletes. `GET` is considered
  **safe**: it must not change anything on the server. A `GET` request that
  deletes something is easily abused, as we will see in the CSRF section.
- The **`Host`** header says which of the many sites on the same server is
  wanted.
- The **`Cookie`** header carries the cookies the browser keeps for that
  site; the session ID is here (the Sessions and Cookies section).
- The **body** carries data such as the password from a form. If this
  request goes unencrypted, all of it is read on the way (eavesdropping
  from the Network Attacks section).

Everything is in the user's hands: the method, path, headers and body can
be written however one likes, even without a browser. **The server cannot
trust anything in the request because "the browser sent it like that".**
This sentence is the foundation of web security; we will come back to it in
the Input Validation section.

## Responses and status codes

The server's response has the same shape; its first line holds a **status
code**. The hundreds digit of the code gives its class:

```python
def status_class(code):
    classes = {1: "info", 2: "success", 3: "redirect",
               4: "client error", 5: "server error"}
    return classes.get(code // 100, "invalid")


for code in [200, 301, 401, 403, 404, 500]:
    print(code, status_class(code))
```

```text
200 success
301 redirect
401 client error
403 client error
404 client error
500 server error
```

Three security-related codes are often mixed up:

- **401 Unauthorized:** "I do not know who you are." Authentication is
  missing or invalid.
- **403 Forbidden:** "I know who you are, but you are not allowed this."
- **404 Not Found:** "There is no such thing."

When even the existence of a resource must be hidden (someone else's
invoice, for example), 404 is returned instead of 403; otherwise the
attacker learns which numbers exist. **500** is a server error, and the
response does **not show** internal details such as a stack trace, a file
path or version information; those give the attacker a map.

## Reading an address correctly

The parts of a URL are the **scheme** (`https`), the **host**, an optional
**port**, the **path** and the **query**. Python's `urllib.parse` module
splits an address into parts (it only processes text and never goes on the
network):

```python
from urllib.parse import urlsplit

for url in ["https://shop.example.com/cart?id=7",
            "http://shop.example.com:8080/login",
            "https://shop.example.com@203.0.113.66/login"]:
    parts = urlsplit(url)
    print(parts.scheme, parts.hostname, parts.port, parts.path)
```

```text
https shop.example.com None /cart
http shop.example.com 8080 /login
https 203.0.113.66 None /login
```

Look at the third address: to the eye it looks like `shop.example.com`, but
the real host is `203.0.113.66`. In a URL the part to the left of the `@`
sign is read as a user name, and the address does not end there. Phishing
links exploit such differences in appearance. Code that makes decisions
about an address (an allow list, a redirect check) splits the address with
a parser and looks at `hostname`, **not by eye or by text search**. This
will matter again in the SSRF section.

## HTTPS: HTTP carried inside TLS

**HTTPS** is the same HTTP messages carried inside an encrypted connection
set up with **TLS** (the TLS Handshake section of the Cryptography module).
TLS provides three things:

<figure class="fig anat">
  <div class="anat-row"><span><b>Confidentiality</b></span><span>The path, headers, cookies and body cannot be read on the way.</span></div>
  <div class="anat-row"><span><b>Integrity</b></span><span>The message cannot be changed on the way without being noticed.</span></div>
  <div class="anat-row"><span><b>Server identity</b></span><span>The certificate shows that the other end really owns that domain name; this is the protection against a man in the middle.</span></div>
  <figcaption>What HTTPS brings. None of the three is in HTTP itself.</figcaption>
</figure>

There are also things HTTPS **does not bring**, and they are often
confused:

<figure class="fig"><div class="versus">
  <div class="ok"><h4>HTTPS says</h4>"This connection is encrypted and the server at the other end owns the domain name in the address bar."</div>
  <div class="no"><h4>HTTPS does not say</h4>"This site is trustworthy." A phishing site can also get a certificate for its own domain name. It does not close the site's own holes (SQL injection, XSS) either. The domain name visited is still visible (in DNS and the TLS handshake).</div>
</div><figcaption>The padlock describes the connection, not the site's intentions.</figcaption></figure>

## Moving from HTTP to HTTPS, and HSTS

If the user types only `shop.example.com` into the address bar, the
browser often goes with plain `http://` first; the server redirects to
`https://` with a `301`. But that **first request** is unencrypted: an
attacker on the road can block the redirect and keep talking to the user
over plain HTTP. This is called **SSL stripping**.

The solution is **HSTS** (HTTP Strict Transport Security). The server adds
a header to its HTTPS response; once the browser has seen it, it **never
tries plain HTTP** for that site, for the given time:

```python
def parse_hsts(value):
    directives = {}
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        name, _, arg = part.partition("=")
        directives[name.strip().lower()] = arg.strip()
    return directives


h = parse_hsts("max-age=31536000; includeSubDomains")
print(h)
print(int(h["max-age"]) // 86400, "days")
```

```text
{'max-age': '31536000', 'includesubdomains': ''}
365 days
```

- **`max-age`** is the time in seconds; 31536000 seconds is a year. A short
  time (a few minutes) makes the protection almost useless.
- **`includeSubDomains`** extends the rule to all subdomains.
- The browser learns the header on the first HTTPS visit; to close the gap
  before that first visit, sites are also added to the **preload** lists
  built into browsers.

The redirect itself is a simple transformation too; everything except the
scheme is kept:

```python
from urllib.parse import urlsplit


def to_https(url):
    parts = urlsplit(url)
    if parts.scheme == "https":
        return url
    query = "?" + parts.query if parts.query else ""
    return "https://" + parts.netloc + parts.path + query


print(to_https("http://shop.example.com/cart?id=7"))
print(to_https("https://shop.example.com/"))
```

```text
https://shop.example.com/cart?id=7
https://shop.example.com/
```

## Mixed content and too much information

- **Mixed content:** if an HTTPS page loads a script or an image over plain
  `http://`, that piece can be changed on the way. Browsers block this for
  scripts; every resource on the page must be `https://`.
- **Headers that say too much:** headers that announce the exact version,
  such as `Server: ExampleServer/2.4.1`, tell the attacker which known hole
  to try. Information that is not needed is not sent.

## Summary

- HTTP is text-based: the **request line** (method, path, version),
  **headers**, an empty line, the **body**.
- `GET` must not change anything on the server; work that changes state is
  done with `POST` and similar methods.
- Every part of a request is in the user's hands; **the server never
  blindly trusts anything in a request.**
- **401** no identity, **403** no permission, **404** does not exist; 404
  to hide existence. An error response shows no internal details.
- Address decisions are made **with a parser**; the part to the left of
  `@` is not the host.
- **HTTPS** = HTTP + TLS: confidentiality, integrity, server identity. It
  does not say the site is trustworthy.
- **HSTS** tells the browser never to try plain HTTP; `max-age` at least a
  year, `includeSubDomains` and preload where needed.
