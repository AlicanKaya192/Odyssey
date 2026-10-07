# Headers and Authentication

So far you got everything you asked for, because the doors you knocked on
were open to everyone. Most real APIs, though, ask at the door **who you
are**: a weather service wants to count your requests, a company API gives
data only to employees, a payment service needs to know who made a payment.

In this section you learn two things: adding **headers** to a request, and
**proving your identity** with headers. Plus one vital habit: **never
writing the key into your code**.

## Two words: authentication and authorization

Two ideas that get mixed up:

- **Authentication:** "Who are you?" Your key, token or password proves it.
- **Authorization:** "Are you allowed to do this?" The question asked once
  it is known who you are.

The two codes from Section 03 correspond exactly to these:

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>401 Unauthorized</h4><p><b>Authentication</b> failed: "I don't know you."<br>The key is missing, wrong or expired.<br>What to do: check your key and the header.</p></div>
    <div class="dim"><h4>403 Forbidden</h4><p>No <b>authorization</b>: "I know you, but you are not allowed."<br>The key is valid, the door is closed.<br>What to do: another permission is needed.</p></div>
  </div>
  <figcaption>The names are misleading: 401 is called "Unauthorized" but it really means "not recognised".</figcaption>
</figure>

## Adding headers to a request: `headers=`

You give requests the headers as a dictionary too:

```python
import requests

BASE = "http://api.odyssey.test"
r = requests.get(BASE + "/books/1", headers={"Accept": "application/json"})
```

requests still adds its own headers (`User-Agent`, `Accept-Encoding`...);
yours join them, or replace them when they have the same name.

## Method 1: an API key

The simplest identity: a long piece of text you get when you sign up for the
API, the **API key**. It is usually sent in a special header. The practice
server's `/stats` endpoint wants a key in the `X-API-Key` header:

```python
r = requests.get(BASE + "/stats")
print(r.status_code, r.json())
# 401 {'error': 'missing or invalid api key'}

r = requests.get(BASE + "/stats", headers={"X-API-Key": "demo-key-123"})
print(r.status_code, r.json())
# 200 {'books': 23, 'authors': 8, 'oldest': 1811, 'newest': 1986}
```

The request without a key got `401`: the server does not know you. With the
header added, `200`.

The header's name differs from API to API: `X-API-Key`, `X-Api-Token`,
`apikey`... Some APIs want the key as a query parameter (`?api_key=...`). The
documentation says which. A header is preferred when possible: addresses get
written into server logs and browser history, and the key should not show up
there.

## Authorization: a valid key is not enough

Let's ask for the admin report with the same key:

```python
r = requests.get(BASE + "/admin/report", headers={"X-API-Key": "demo-key-123"})
print(r.status_code, r.json())
# 403 {'error': 'this key cannot read admin reports'}
```

This time `403`: the server knows you, but this door is closed to you. With
`401` you check your key; with `403` you need another **permission**;
sending the same request again changes nothing.

## Method 2: a bearer token

A very common second way is sending a **token** in the `Authorization`
header:

```python
r = requests.get(BASE + "/me", headers={"Authorization": "Bearer letmein"})
print(r.status_code, r.json())
# 200 {'user': 'ada', 'role': 'editor'}
```

The header's value has two parts: the word `Bearer`, a space and the token.
"Bearer" means "carrier": **whoever carries this token is authorized**. That
is why a token must be kept like a key; whoever gets hold of it can send
requests in your place.

The most common mistake is forgetting the `Bearer ` prefix:

```python
r = requests.get(BASE + "/me", headers={"Authorization": "letmein"})
print(r.status_code)   # 401
```

Tokens are usually obtained with a login request and **expire** after a
while. With an expired token you get `401`; you need a new one. The details of
that flow (such as OAuth) differ from API to API and are described in the
documentation.

## Method 3: user name and password (Basic)

An old but still common way is **Basic** authentication: a user name and a
password. requests offers the `auth=` parameter for it:

```python
r = requests.get(BASE + "/basic", auth=("reader", "pass123"))
print(r.status_code, r.json())             # 200 {'user': 'reader'}
print(r.request.headers["Authorization"])  # Basic cmVhZGVyOnBhc3MxMjM=
```

requests encodes the text `reader:pass123` with **base64** and puts it in the
`Authorization` header. Base64 is **not** encryption; anyone can decode it.
That is why Basic is only used with `https`.

## Do not write the key into the code

This line will cause trouble one day:

```python
API_KEY = "sk_live_8f2a..."   # don't
```

The code goes to GitHub, to a friend, into a screenshot, and the key goes with
it. With a leaked key someone else sends requests in your name, your bill
grows or your data is exposed. And a key that was committed once stays in the
history even after you delete it.

The right way is keeping the key in an **environment variable**. Environment
variables are name-value pairs the operating system gives a program; they live
apart from the code:

```python
import os

key = os.environ.get("LIBRARY_KEY", "demo-key-123")
r = requests.get(BASE + "/stats", headers={"X-API-Key": key})
```

`os.environ.get(name, default)` reads the variable; if it is not defined it
gives the default. In the exercises we use the practice server's public key as
the default; in a real project you **do not** set a default: if the key is
missing, the program should stop and say so.

Defining an environment variable from the command line on Windows:

```text
set LIBRARY_KEY=your-real-key
python program.py
```

In projects, keys are often kept in a file called `.env`, and that file is
**never** added to git (`.gitignore`).

## The same header on every request: `Session`

Writing the same key on every request is long and error-prone.
`requests.Session` opens a **session**: the headers you give it are added to
every request in the session.

```python
session = requests.Session()
session.headers.update({
    "Authorization": "Bearer letmein",
    "User-Agent": "odyssey-notes/1.0",
})

print(session.get(BASE + "/me").json())   # {'user': 'ada', 'role': 'editor'}
print(session.get(BASE + "/books/1").request.headers["User-Agent"])   # odyssey-notes/1.0
```

A session has one more benefit: requests to the same server reuse the same
connection, which speeds things up when there are many requests.

## `User-Agent`: introduce yourself

requests adds a header such as `User-Agent: python-requests/2.34.2` to every
request. Some APIs ask you to write your own name to see who is sending
requests: `User-Agent: odyssey-notes/1.0 (ada@example.com)`. So they can reach
you if there is a problem. A polite habit.

## Summary

- **Authentication** is "who are you", **authorization** "are you allowed".
  `401` you are not recognised, `403` not allowed.
- Headers are added with `headers={...}`.
- An **API key** usually goes in a header (`X-API-Key`); a **bearer token**
  in `Authorization: Bearer <token>`; **Basic** with `auth=(name, password)`.
- Whoever carries the token or key is authorized; keep them safe. Basic only
  with `https`.
- Do not write the key into the code: read it from an environment variable
  with `os.environ.get(...)`, and never add the `.env` file to git.
- `requests.Session()` adds headers to every request and reuses the
  connection.
