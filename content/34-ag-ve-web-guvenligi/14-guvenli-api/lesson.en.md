# Secure APIs

The web sections so far mostly looked at pages the browser shows. Most of
today's applications, however, talk through an **API**: a phone app, a
script in the browser or another server sends JSON to an address and gets
JSON back. There is no page; but most of the problems we saw on pages
exist in APIs too, and some become easier to see, because the attacker
writes the request directly. This section shows API-specific mistakes and
their defences with small Python functions that run in memory; no network
connection is made.

Next to OWASP's Top 10 list for web applications, there is a separate list
for APIs (the **API Security Top 10**). We start with the mistake at the
top of that list.

## Object level authorization

In an API, resources are usually asked for by an id: `GET /orders/2`. The
person writing the request picks the id. If the server only checks "is
this person logged in?" and not "is this order this person's?", anyone can
read someone else's order by changing the number:

```python
ORDERS = {
    1: {"owner": "ada", "total": 40},
    2: {"owner": "bob", "total": 75},
}


def get_order_leaky(user, order_id):
    return ORDERS.get(order_id)


def get_order(user, order_id):
    order = ORDERS.get(order_id)
    if order is None or order["owner"] != user:
        return 404, None
    return 200, order


print(get_order_leaky("ada", 2))
print(get_order("ada", 2))
print(get_order("ada", 1))
```

```text
{'owner': 'bob', 'total': 75}
(404, None)
(200, {'owner': 'ada', 'total': 40})
```

The first function gave `ada` the order of `bob`. This mistake is called
**Broken Object Level Authorization** (BOLA); its name in the web list is
**IDOR** (Insecure Direct Object Reference). It is the most common form in
APIs of the "broken access control" from the OWASP Top 10 section.

The defence is to check ownership at **every** endpoint that fetches an
object. Two details matter:

- Returning `404` (not found) instead of `403` (forbidden) for someone
  else's order does not reveal whether the order exists either.
- Ids that increase one by one make guessing easy; random ids
  (`secrets.token_hex`) make it harder but **do not replace the check**. An
  unguessable id also shows up one day in a log or a shared link.

<figure class="fig">
<div class="flow">
<span class="node">request: GET /orders/2</span>
<span class="arrow">→</span>
<span class="node">who? (authentication)</span>
<span class="arrow">→</span>
<span class="node acc">is this object theirs?</span>
<span class="arrow">→</span>
<span class="node ok">response</span>
</div>
<figcaption>Authentication answers "who"; authorization is asked separately for every object.</figcaption>
</figure>

## Assigning extra fields

If a profile update endpoint writes the incoming JSON into the record as
it is, the person writing the request can also send fields that are not in
the form at all:

```python
def update_leaky(user, body):
    user.update(body)
    return user


ALLOWED = {"name", "email"}


def update_safe(user, body):
    rejected = sorted(set(body) - ALLOWED)
    for key in ALLOWED & set(body):
        user[key] = body[key]
    return user, rejected


body = {"name": "Ada L", "role": "admin"}
print(update_leaky({"name": "Ada", "role": "user"}, body))
print(update_safe({"name": "Ada", "role": "user"}, body))
```

```text
{'name': 'Ada L', 'role': 'admin'}
({'name': 'Ada L', 'role': 'user'}, ['role'])
```

`update_leaky` made the user an administrator at their own request. This
mistake is called **mass assignment**. The defence is an **allow list**:
only the fields that may be changed are copied. Instead of quietly
dropping the rejected fields, refusing with `422` is an option too; the
client sees its mistake.

## Sending too much data

The same problem has a reverse direction: the server sends the whole
record and thinks "the client will show what is needed". But the whole
JSON is in the client's hands:

```python
user = {
    "id": 7,
    "name": "Ada",
    "email": "ada@example.com",
    "password_hash": "pbkdf2$...",
    "is_admin": False,
}
PUBLIC = ["id", "name"]


def public_view(record):
    return {key: record[key] for key in PUBLIC}


print(sorted(user))
print(public_view(user))
```

```text
['email', 'id', 'is_admin', 'name', 'password_hash']
{'id': 7, 'name': 'Ada'}
```

Only two of the record's five fields need to be shown to others. The
response is always built from **explicitly chosen** fields; the record
object is not turned into JSON as it is. In the API Security Top 10 these
two mistakes (assigning too much, showing too much) are gathered under one
heading: **Broken Object Property Level Authorization**.

<figure class="fig">
<div class="versus">
<div class="no">
<h4>The record as it is</h4>
<p>Incoming JSON is written to the record, the record is turned into JSON
and sent. When a field is added, it opens to the outside without anyone
noticing.</p>
</div>
<div class="ok">
<h4>With an allow list</h4>
<p>Only changeable fields on the way in, only showable fields on the way
out. A new field is closed by default.</p>
</div>
</div>
<figcaption>An allow list in both directions: a new field does not open to the outside by itself.</figcaption>
</figure>

## Request limits

A single client can send thousands of requests a second to an unlimited
API: trying passwords, scraping data or wearing out the server. The
**token bucket** is a commonly used limit: the bucket holds at most
`capacity` tokens, each request spends one token, and the bucket fills
with `rate` tokens every second:

```python
def make_bucket(capacity, rate):
    state = {"tokens": capacity, "last": 0}

    def allow(now):
        elapsed = now - state["last"]
        state["tokens"] = min(capacity, state["tokens"] + elapsed * rate)
        state["last"] = now
        if state["tokens"] >= 1:
            state["tokens"] -= 1
            return True
        return False

    return allow


allow = make_bucket(capacity=3, rate=1)
times = [0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3]
print("".join("+" if allow(t) else "-" for t in times))
```

```text
+++--+-++--
```

`+` is a request let through, `-` one turned away. The first three of the
five requests at second 0 spent the three tokens in the bucket; at second
1 one token had arrived, and the second request was turned away again; at
second 3, two requests got through with two seconds' worth of tokens. The
bucket allows short bursts but keeps the average rate at `rate` over time.
A turned-away request gets `429 Too Many Requests`, optionally with a
`Retry-After` header.

The limit is not only for the number of requests: the body's size, the
number of records returned on one page (`?limit=100000`) and the work a
single request triggers are limited too. In the API Security Top 10 this
heading is called **Unrestricted Resource Consumption**.

## API keys

In APIs where one server talks to another, the client is usually
recognised by an **API key**. A key is a password and is protected like
one: the server stores a hash of the key, not the key itself, and compares
in constant time:

```python
import hashlib
import hmac

stored = hashlib.sha256(b"k_demo_7f3a").hexdigest()


def check_key(given):
    digest = hashlib.sha256(given.encode()).hexdigest()
    return hmac.compare_digest(digest, stored)


print(stored[:16])
print(check_key("k_demo_7f3a"), check_key("k_demo_0000"))
```

```text
87afbccd80d0a41c
True False
```

The key in the example is short so it is readable; a real key is
generated long and random, like `secrets.token_urlsafe(32)`. Because a
long random key cannot be guessed, unlike a password it does not need a
slow hash (`pbkdf2`); a single SHA-256 is enough. `hmac.compare_digest`
keeps the comparison's time from depending on which character the two
differ at.

The key is sent in a header (`Authorization`), not in the address:
addresses end up in server logs, browser history and proxy servers.

## Signing the request

A key only answers "who". To show that the request was **not changed** on
the way and **not replayed**, the request is signed with a secret both
sides know (HMAC from the Cryptography module). Time goes into the
signature too; the server does not accept an old request:

```python
import hashlib
import hmac

SECRET = b"shared-demo-secret"


def sign(ts, method, path, body):
    message = f"{ts}\n{method}\n{path}\n{body}".encode()
    return hmac.new(SECRET, message, hashlib.sha256).hexdigest()


def verify(ts, now, method, path, body, signature):
    if abs(now - ts) > 300:
        return "expired"
    expected = sign(ts, method, path, body)
    if not hmac.compare_digest(expected, signature):
        return "bad signature"
    return "ok"


sig = sign(1000, "POST", "/transfer", '{"amount": 10}')
print(verify(1000, 1030, "POST", "/transfer", '{"amount": 10}', sig))
print(verify(1000, 1030, "POST", "/transfer", '{"amount": 99}', sig))
print(verify(1000, 2000, "POST", "/transfer", '{"amount": 10}', sig))
```

```text
ok
bad signature
expired
```

When the amount in the body changed, the signature did not hold; when the
same request was sent 1000 seconds later, it counted as expired. The
300-second window leaves room for the small difference between two
machines' clocks. To also stop the same request arriving a second time
inside the window, the request carries a random value used only once (a
**nonce**), and the server remembers the ones it saw for the length of the
window.

## Error responses

An API should tell the client about an error but not give internal
details. A stack trace, a database error text or a file path shows the
attacker the inside of the system. A short code and message go to the
client (`{"error": "not_found"}`), the details go to the log; to link the
two, a request id can be added to the response.

## Summary

- Authentication answers "who", authorization answers "is this object
  theirs"; the second is asked at **every** endpoint, for every object.
- Fields are chosen with an **allow list** on the way in and on the way
  out.
- The number of requests, the body size and the page size are limited;
  the token bucket allows bursts and keeps the average.
- An API key is generated long and random, its hash is stored, it is sent
  in a header and compared in constant time.
- A signature (HMAC + time + nonce) catches a changed and a replayed
  request.
