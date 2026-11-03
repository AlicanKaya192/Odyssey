# CSRF: Cross-Site Request Forgery

In the Sessions and Cookies section we saw that the browser sends the
session cookie back **with every request**. This convenience has a price:
the browser attaches the cookie **without looking at where the request was
started**. While a user is logged in to their bank, a page on another site
can make their browser send a request to the bank; because the cookie is
attached automatically, the bank thinks the request came from the user.
This is called **CSRF** (cross-site request forgery). This section shows
the hole with an imitation browser, then builds its defences: the CSRF
token, the `SameSite` cookie, origin checks and a `GET` that changes no
state. All the "sites" are Python dictionaries; no request is sent.

## The hole: the cookie goes by itself

Let us imitate a browser and a bank server with small functions. The
browser's cookie jar holds the bank's session cookie:

```python
jar = {"bank.example": {"session": "s-ada"}}
SESSIONS = {"s-ada": "ada"}
BALANCE = {"ada": 1000}


def server(path, form, cookies):
    user = SESSIONS.get(cookies.get("session"))
    if user is None:
        return "401 login required"
    if path == "/transfer":
        BALANCE[user] -= int(form["amount"])
        return f"200 sent {form['amount']} to {form['to']}"
    return "404"


def browser_send(target, path, form, from_site):
    cookies = jar.get(target, {})
    return server(path, form, cookies)


print(browser_send("bank.example", "/transfer",
                   {"to": "bob", "amount": "50"}, "bank.example"))
print(browser_send("bank.example", "/transfer",
                   {"to": "mallory", "amount": "900"}, "games.example"))
print(BALANCE["ada"])
```

```text
200 sent 50 to bob
200 sent 900 to mallory
50
```

Ada sent the first request from the bank's own page. The second was
started by a hidden form on a games site Ada had open at the time; the
browser attached the bank's cookie without looking at `from_site` at all,
and the server could not tell the two requests apart. Ada's balance fell
to 50.

Note three things:

- The attacker **did not see** Ada's cookie and did not steal it. They only
  made the browser send a request.
- The attacker **cannot see the response** either: the browser stops one
  site from reading another site's response (the same-origin policy, the
  CORS and Security Headers section). That is why CSRF is used not to read
  data but **to get an action done**: sending money, changing the e-mail
  address, changing the password.
- The only question the server asked was "is this cookie valid?". The
  question it should ask is "did the user send this request **from our
  page**?".

## The first defence: the CSRF token

When the server puts the action form onto the page, it adds an
unpredictable **token** to it and ties the token to the session. When the
form is sent, the token is checked. Another site cannot know this token:
since it cannot read the bank's page, it cannot see the token inside it.

```python
import hmac
import secrets

csrf_tokens = {}


def new_form(session_id):
    token = secrets.token_urlsafe(32)
    csrf_tokens[session_id] = token
    return token


def check(session_id, form):
    expected = csrf_tokens.get(session_id)
    sent = form.get("csrf", "")
    return expected is not None and hmac.compare_digest(expected, sent)


token = new_form("s-ada")
print(check("s-ada", {"to": "bob", "amount": "50", "csrf": token}))
print(check("s-ada", {"to": "mallory", "amount": "900"}))
print(check("s-ada", {"to": "mallory", "amount": "900", "csrf": "guess"}))
```

```text
True
False
False
```

The request from the bank's own form passed; the requests with no token or
a wrong token were refused. The token is made with `secrets` (like the
session ID in the Sessions and Cookies section) and compared with
`hmac.compare_digest`. Applications that do not want to store it on the
server can also keep the token in a cookie and compare it with the one in
the form (the **double-submit cookie**); the idea is the same: another
site cannot know the value in the form.

The token is checked only on requests that change state (`POST`, `PUT`,
`PATCH`, `DELETE`); that is why the rule below matters.

## The second defence: the SameSite cookie

We saw the `SameSite` attribute in the Sessions and Cookies section. The
browser looks at this attribute to decide whether to attach the cookie to a
request started from another site:

```python
def sends_cookie(samesite, cross_site, method, top_level):
    if not cross_site:
        return True
    if samesite == "Strict":
        return False
    if samesite == "Lax":
        return method == "GET" and top_level
    return True


cases = [("Strict", "POST", False), ("Lax", "POST", False),
         ("Lax", "GET", True), ("None", "POST", False)]
for samesite, method, top in cases:
    print(f"{samesite:<6} {method:<4} top={top!s:<5} -> "
          f"{sends_cookie(samesite, True, method, top)}")
```

```text
Strict POST top=False -> False
Lax    POST top=False -> False
Lax    GET  top=True  -> True
None   POST top=False -> True
```

- **`Strict`:** no request started from another site gets the cookie. The
  safest; but a user arriving through a link from another site looks
  logged out on the first page.
- **`Lax`:** from another site, the cookie is attached only to **top-level
  navigation** (clicking a link so the page changes) with `GET`. A `POST`
  sent with a hidden form goes without the cookie. A good default for a
  session cookie.
- **`None`:** attached to every request (accepted only together with
  `Secure`). For cookies that really need to be used on other sites.

Some browsers treat a cookie without the attribute as `Lax`, but this is
not relied on; the attribute is written explicitly. `SameSite` is a strong
**second layer** and does not replace the token: old browsers do not know
it, and a subdomain of the same site counts as "the same site".

## GET changes no state

Look at the `Lax` row: on a top-level `GET` from another site the cookie
goes along. If an address such as `GET /transfer?to=mallory&amount=900`
sends money, all the attacker has to do is get the user to click that
link. The rule from the HTTP and HTTPS section is vital here: **`GET`
changes nothing on the server.** Every action that changes state is done
with a method like `POST` and with a token.

## The third defence: origin checks

Browsers add an `Origin` header to `POST` requests started from another
site, telling which **origin** (scheme + host + port) the request came
from; the page itself cannot change this header. On requests that change
state the server compares this header with an allow list:

```python
ALLOWED = {"https://bank.example"}


def origin_ok(headers):
    return headers.get("origin") in ALLOWED


print(origin_ok({"origin": "https://bank.example"}))
print(origin_ok({"origin": "https://games.example"}))
print(origin_ok({}))
```

```text
True
False
False
```

What to do if the header is missing is decided in advance: either the
origin of the `Referer` header is checked or the request is refused. The
origin check is also a layer next to the token.

## Re-authentication for important actions

For actions such as changing the password, changing the e-mail address or a
large payment, the user is asked for their **password** or an MFA code
again. Another site does not know the user's password, so it cannot pass
this step.

## CSRF and XSS

All CSRF defences rest on the assumption "the request comes **from another
site**". If the site has an XSS hole, the leaked script runs **inside the
site itself**: it reads the token on the page, the `Origin` looks right,
`SameSite` does not stop it. That is why an XSS hole also defeats CSRF
defences; the two holes are closed together.

## Summary

- **CSRF:** the browser attaches the cookie without looking at where the
  request started; another site **gets an action done** in the user's name
  (it cannot read the response).
- **CSRF token:** a value tied to the session, made with `secrets`, sent in
  the form and checked with `compare_digest`; another site cannot know it.
- **SameSite:** `Lax` attaches no cookie to a `POST` from another site,
  `Strict` to no request at all. Written explicitly; it does not replace
  the token.
- **`GET` changes no state;** `Lax` attaches the cookie to a top-level
  `GET`.
- **Origin check:** the `Origin` header is compared with an allow list.
- For important actions the password or MFA is asked again.
- An XSS hole defeats CSRF defences.
