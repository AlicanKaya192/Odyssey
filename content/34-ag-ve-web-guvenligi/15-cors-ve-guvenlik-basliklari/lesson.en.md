# CORS and Security Headers

By default the browser stops a script running on one site's page from
reading data from another site. This rule is called the **same-origin
policy** and it is a cornerstone of web security: otherwise any open tab
could read the information on your bank's page. Sometimes this rule needs
to be loosened on purpose (when the site's own API sits at a separate
address); the way to do that is **CORS**. This section shows how CORS
works, the most common configuration mistakes, and the **security
headers** the server sends to the browser, with small Python functions.

## What is an origin?

An **origin** has three parts: scheme, domain name and port. If all three
are the same, two addresses are of the same origin; the path does not
matter:

```python
from urllib.parse import urlsplit

DEFAULT_PORTS = {"http": 80, "https": 443}


def origin(url):
    parts = urlsplit(url)
    port = parts.port or DEFAULT_PORTS[parts.scheme]
    return parts.scheme, parts.hostname, port


base = "https://shop.example/cart"
for other in [
    "https://shop.example:443/account",
    "http://shop.example/cart",
    "https://api.shop.example/cart",
    "https://shop.example:8443/cart",
]:
    print(origin(base) == origin(other), other)
```

```text
True https://shop.example:443/account
False http://shop.example/cart
False https://api.shop.example/cart
False https://shop.example:8443/cart
```

When no port is written, 443 counts for HTTPS; that is why the first
address is the same origin. When the scheme (`http`), the subdomain
(`api.`) or the port (`8443`) changes, the origin changes. A subdomain is
a separate origin too: `api.shop.example` cannot read the pages of
`shop.example`.

The same-origin policy blocks **reading**, not **sending**: another
site's form can send a request to your site. That is why the CSRF section
needed a token and `SameSite`.

## CORS: the server grants permission

When the browser sends a request to another origin, it puts an `Origin`
header in the request. If the server grants this origin read permission
with `Access-Control-Allow-Origin` in its response, the browser hands the
response to the script; if not, the script cannot see the response. The
**server** decides, the **browser** enforces.

The most dangerous mistake is writing the incoming `Origin` back as it is,
especially together with cookies:

```python
def cors_leaky(origin):
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
    }


ALLOWED_ORIGINS = {"https://shop.example", "https://admin.shop.example"}


def cors_safe(origin):
    headers = {"Vary": "Origin"}
    if origin in ALLOWED_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return headers


for origin in ["https://shop.example", "https://other.example"]:
    print(origin)
    print("  leaky:", cors_leaky(origin)["Access-Control-Allow-Origin"])
    print("  safe: ", cors_safe(origin).get("Access-Control-Allow-Origin"))
```

```text
https://shop.example
  leaky: https://shop.example
  safe:  https://shop.example
https://other.example
  leaky: https://other.example
  safe:  None
```

`cors_leaky` gave every site permission to "read with cookies": when the
user opens any page, that page's script can read data from your API with
the user's session. The same-origin policy is gone entirely. `cors_safe`
only allows origins on the **allow list**.

The `Vary: Origin` header tells a cache in between that the response
changes with `Origin`; otherwise a response given to one origin could be
returned from the cache to another origin too. The browser does not
accept a request with cookies with `Access-Control-Allow-Origin: *`
anyway; `*` is only suitable for public data that needs no identity.

## Checking the allow list with text

Saying "if it ends with our domain name" instead of an allow list looks
tempting, but it also accepts **another** domain name that ends the same
way:

```python
def allowed_suffix(origin):
    return origin.endswith("shop.example")


def allowed_exact(origin):
    return origin in ALLOWED_ORIGINS


ALLOWED_ORIGINS = {"https://shop.example", "https://admin.shop.example"}
for origin in ["https://admin.shop.example", "https://notshop.example"]:
    print(f"{origin:<27} {allowed_suffix(origin)!s:<5} {allowed_exact(origin)}")
```

```text
https://admin.shop.example  True  True
https://notshop.example     True  False
```

`notshop.example` is not our domain name, but it ends with
`shop.example`. Origins are checked with **exact equality** against a
set; if a pattern is needed, including the dot (`.shop.example`) and with
the scheme, with `re.fullmatch`. The value `Origin: null` does not go on
the allow list either: pages opened from a file and some redirects send
this value.

## The preflight request

The browser first asks about some requests with a **preflight** request:
with the `OPTIONS` method, "may I send a request from this origin, with
this method, with these headers?" Simple requests (`GET`, `HEAD`, `POST`
and the three content types forms can send) go without asking:

```python
SIMPLE_METHODS = {"GET", "HEAD", "POST"}
SIMPLE_TYPES = {
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
}


def needs_preflight(method, content_type):
    return method not in SIMPLE_METHODS or content_type not in SIMPLE_TYPES


print(needs_preflight("POST", "text/plain"))
print(needs_preflight("POST", "application/json"))
print(needs_preflight("DELETE", "text/plain"))
```

```text
False
True
True
```

A `POST` that sends JSON and a `DELETE` are asked about first. This detail
matters for CSRF: a form on another site cannot send
`application/json`, but it can send a `POST` with `text/plain`. If the
server only accepts `Content-Type: application/json` requests, it also
indirectly keeps out requests from other origins that cannot pass the
preflight. Still, this does not replace a CSRF token; it is an extra
layer.

<figure class="fig">
<div class="flow">
<span class="node">script: fetch(api)</span>
<span class="arrow">→</span>
<span class="node">OPTIONS + Origin</span>
<span class="arrow">→</span>
<span class="node acc">did the server allow it?</span>
<span class="arrow">→</span>
<span class="node ok">actual request</span>
</div>
<figcaption>For a request that needs a preflight, the browser asks for permission first; without permission the actual request is never sent.</figcaption>
</figure>

## Security headers

With every response the server can also send the browser instructions on
"how should I protect this page?". A small function that checks the
headers in a response:

```python
REQUIRED = [
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "referrer-policy",
    "x-frame-options",
]

response = {
    "Content-Type": "text/html; charset=utf-8",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
}

present = {name.lower() for name in response}
for name in REQUIRED:
    if name not in present:
        print("missing:", name)
```

```text
missing: content-security-policy
missing: referrer-policy
missing: x-frame-options
```

Three of the five headers are missing. Header names are case-insensitive;
that is why the comparison was done in lower case. What the headers do:

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Content-Security-Policy</span><span>Which sources scripts, styles and images may be loaded from (the XSS section).</span></div>
<div class="anat-row"><span>Strict-Transport-Security</span><span>For a while the browser connects to this site only over HTTPS (the HTTP and HTTPS section).</span></div>
<div class="anat-row"><span>X-Content-Type-Options: nosniff</span><span>The browser follows the declared type and does not guess a type from the content.</span></div>
<div class="anat-row"><span>Referrer-Policy</span><span>How much of the address is sent when moving to another site.</span></div>
<div class="anat-row"><span>X-Frame-Options / frame-ancestors</span><span>Stops the page from being shown inside another site's frame.</span></div>
</div>
<figcaption>Five common security headers and their jobs.</figcaption>
</figure>

Blocking frames is against **clickjacking**: the attacker puts your page
in an invisible frame over their own page and makes the user click your
button without knowing. Today the same job is also done with CSP's
`frame-ancestors 'none'` directive; sending both covers older browsers
too.

Headers do not fix the application's own mistakes: CSP does not replace
a template without escaping; HSTS does not replace a login left open on
HTTP. They are all a **second layer**.

## Summary

- Origin = scheme + domain name + port; the same-origin policy blocks
  **reading** from another origin.
- With CORS, the server grants permission; writing the incoming `Origin`
  back, especially with `Allow-Credentials: true`, removes the policy.
- Origins are checked with exact equality against an allow list;
  `endswith` and `null` are traps. `Vary: Origin` is not forgotten.
- Requests that send JSON and other non-simple requests are first asked
  about with a preflight.
- CSP, HSTS, `nosniff`, `Referrer-Policy` and frame blocking have the
  browser build a second layer of defence.
