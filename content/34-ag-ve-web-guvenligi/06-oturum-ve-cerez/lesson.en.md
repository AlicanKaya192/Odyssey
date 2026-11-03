# Sessions and Cookies

HTTP is **stateless**: every request is independent of the previous one,
and the server does not know by itself whether a request comes from the
person who just logged in. To avoid asking for the password on every page,
a **session** is used: when login succeeds, the server gives the person a
**session ID**, and the browser keeps it in a **cookie** and sends it back
with every request. From then on this ID stands in for the password;
whoever gets hold of it enters the account without knowing the password.
This section explains how to generate a session ID, how to protect the
cookie and when to end the session.

## The session ID

The server maps the ID to the person in a dictionary (in reality a
database). The ID must be **unpredictable**; that is what the `secrets`
module from the Randomness section of the Cryptography module is for:

```python
import secrets

sessions = {}


def login(user):
    sid = secrets.token_urlsafe(32)
    sessions[sid] = {"user": user}
    return sid


sid = login("ada")
print(len(sid))
print(sessions[sid]["user"])
```

```text
43
ada
```

`token_urlsafe(32)` turns 32 random bytes (256 bits) into a 43-character
text that is safe to use in a URL. It is impossible to guess. Generating
the ID with a counter, on the other hand, is a serious mistake:

```python
counter = 1000


def weak_login(user):
    global counter
    counter += 1
    return f"s{counter}"


print(weak_login("ada"), weak_login("bob"))
```

```text
s1001 s1002
```

Someone whose own ID is `s1001` knows that the next user will get `s1002`;
they change their cookie and enter that session. IDs made from a
timestamp, the user name or the `random` module can be guessed for the same
reason.

## The cookie and its attributes

The server sets a cookie with a response header:
`Set-Cookie: session=...`. The **attributes** added at the end of the header say how the
cookie is protected:

<figure class="fig anat">
  <div class="anat-row"><span><b>Secure</b></span><span>The cookie is sent only over HTTPS; it is not read on the way over plain HTTP.</span></div>
  <div class="anat-row"><span><b>HttpOnly</b></span><span>JavaScript on the page cannot reach the cookie; stealing it with XSS becomes harder (the XSS section).</span></div>
  <div class="anat-row"><span><b>SameSite</b></span><span>Whether the cookie is sent on requests started from another site: <code>Strict</code>, <code>Lax</code>, <code>None</code>. Against CSRF (the CSRF section).</span></div>
  <div class="anat-row"><span><b>Max-Age / Expires</b></span><span>How long the cookie lives. Without it, it is deleted when the browser closes.</span></div>
  <div class="anat-row"><span><b>Path / Domain</b></span><span>Which paths and domain names the cookie is sent to. The wider <code>Domain</code> is, the more subdomains see the cookie.</span></div>
  <figcaption>On a session cookie, Secure, HttpOnly and SameSite are almost always on.</figcaption>
</figure>

Let us split a `Set-Cookie` header and find the missing attributes:

```python
def cookie_flags(header):
    parts = [p.strip() for p in header.split(";")]
    name = parts[0].partition("=")[0]
    flags = {}
    for p in parts[1:]:
        key, _, value = p.partition("=")
        flags[key.lower()] = value
    return name, flags


for header in ["session=abc123; Path=/",
               "session=abc123; Path=/; Secure; HttpOnly; SameSite=Lax"]:
    name, flags = cookie_flags(header)
    missing = [f for f in ["secure", "httponly", "samesite"] if f not in flags]
    print(name, "missing:", missing)
```

```text
session missing: ['secure', 'httponly', 'samesite']
session missing: []
```

The first cookie lacks all three protections: it is read on the way on a
plain HTTP page, a script that leaks into the page can read it, and it is
attached to requests started from other sites. The second is set up
correctly.

## Session fixation

If an attacker can plant a session ID of their own choosing in the
victim's browser (for example by setting a cookie from a subdomain) and the
server keeps using **the same ID** after login, then the moment the victim
logs in, the ID the attacker knows becomes an authorised session. This is
called **session fixation**. Its defence is simple: **the ID is renewed at
login.**

```python
import secrets

sessions = {}


def login_keep(sid, user):
    sessions[sid] = user
    return sid


def login_rotate(sid, user):
    sessions.pop(sid, None)
    new_sid = secrets.token_urlsafe(32)
    sessions[new_sid] = user
    return new_sid


planted = "attacker-chosen-id"
print(login_keep(planted, "ada") == planted)
print(login_rotate(planted, "ada") == planted, planted in sessions)
```

```text
True
False False
```

With the first method the attacker's ID is still valid after login. With
the second, the old ID was deleted and replaced by a new one that nobody
knows. The same rule applies when privileges change: when the person
becomes an administrator or changes their password, the ID is renewed.

## The end of a session

A session must not stay valid forever. The shorter a stolen ID lives, the
less harm it does. Two times are used:

- **Idle timeout:** if a certain time has passed since the last request,
  the session ends (a computer left open on the desk).
- **Absolute timeout:** even if the person keeps working, if a certain time
  has passed since login, a new login is required.

```python
IDLE, ABSOLUTE = 15 * 60, 8 * 3600


def still_valid(created, last_seen, now):
    return now - last_seen < IDLE and now - created < ABSOLUTE


print(still_valid(0, 0, 600))
print(still_valid(0, 0, 1200))
print(still_valid(0, 28700, 28900))
```

```text
True
False
False
```

After 10 minutes the session is valid; after 20 minutes idle it is not. In
the third case the person did something 200 seconds ago, but more than 8
hours have passed since login; the session is over.

**Logout** is not just deleting the cookie in the browser: the server
deletes the session record too. Otherwise someone who took a copy of the
cookie carries on after logout.

## Keeping state in the cookie: signed cookies

Some applications keep the session information not on the server but in
the cookie **itself** (`user=ada;role=user`). Because the user can change
the cookie at will, this information **must be signed**. The tag from the
HMAC section does exactly this:

```python
import hashlib
import hmac

KEY = b"server-only-secret"


def sign(value):
    tag = hmac.new(KEY, value.encode(), hashlib.sha256).hexdigest()
    return value + "." + tag


def read(cookie):
    value, _, tag = cookie.rpartition(".")
    expected = hmac.new(KEY, value.encode(), hashlib.sha256).hexdigest()
    return value if hmac.compare_digest(tag, expected) else None


cookie = sign("user=ada;role=user")
print(read(cookie))
print(read(cookie.replace("role=user", "role=admin")))
```

```text
user=ada;role=user
None
```

When the user changed their role to `admin`, the tag did not match and the
cookie was rejected (`None`). The signature does not **hide** the
information, it only stops it being changed; everything in the cookie can
be read. Nothing secret is written into a cookie. A signed cookie also has
a weakness: the server cannot invalidate it on its own; it stays valid
until it expires. That is why an expiry time is put inside it.

## Summary

- HTTP is stateless; after login the **session ID** stands in for the
  password. Whoever steals it enters the account.
- The ID is generated with `secrets` (`token_urlsafe(32)`, 256 bits); an ID
  made from a counter, the time or `random` can be guessed.
- On the session cookie, **Secure**, **HttpOnly** and **SameSite** are on.
- Against **session fixation**, the ID is renewed at login (and when
  privileges change).
- A session ends with an **idle** and an **absolute** timeout; at logout
  the record on the server is deleted too.
- If state is kept in a cookie, it is **signed** (HMAC); a signature does
  not hide, and secret information is not written into a cookie.
