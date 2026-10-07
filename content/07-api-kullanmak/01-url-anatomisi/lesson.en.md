# Anatomy of an Address: the URL

Every request goes to an **address**. The one you type into the browser's
address bar and the one a program sends to an API are the same kind of
address: a **URL** (Uniform Resource Locator, "the address that shows where a
resource is").

At first sight a URL looks like a single piece of text. In fact it has six
parts, and each part has its own job. Building those parts correctly is what
you will do most often when using an API; a badly built address means a
request that never reaches the server or asks for the wrong thing.

## The parts of a URL

Let's take this address apart:

```text
https://api.example.com:8443/v1/weather?city=Istanbul&units=metric#today
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Scheme</span><span><code>https</code>: the rules of the talk; <b>s</b> means encrypted</span></div>
    <div class="anat-row"><span>Host</span><span><code>api.example.com</code>: the computer the request goes to</span></div>
    <div class="anat-row"><span>Port</span><span><code>8443</code>: which program on that computer is listening</span></div>
    <div class="anat-row"><span>Path</span><span><code>/v1/weather</code>: which endpoint</span></div>
    <div class="anat-row"><span>Query string</span><span><code>city=Istanbul&amp;units=metric</code>: extra details</span></div>
    <div class="anat-row"><span>Fragment</span><span><code>today</code>: for the browser only, never reaches the server</span></div>
  </div>
  <figcaption>Six parts, six separate jobs. In an API request you mostly deal with the path and the query string.</figcaption>
</figure>

Now let's look at each part one by one.

## Scheme: which language to speak

The `https://` part is the **scheme**. It says by which rules the client and
the server will talk.

- `http`: plain talk. Anyone who gets in the way can read everything.
- `https`: the same talk, but **encrypted**. The final **s** stands for
  "secure".

APIs almost always use `https`, because requests often carry a password or a
key. You only connect with `http` to a server you are trying out on your own
computer.

## Host: who is being asked

`api.example.com` is the **host**: the name of the computer the request goes
to. Every computer on the internet has an address made of numbers; this
readable name is translated into that number.

Many companies put their API under a separate name: the site is
`example.com`, the API is `api.example.com`. The leading `api.` is a
**subdomain**.

Learn one special host name now: **`localhost`** (or `127.0.0.1`) means
**your own computer**. The server you write in API 2 and the practice server
you will send requests to on this path will run there.

## Port: the flat number in the building

`:8443` is the **port**. If the host is a block of flats, the port is the
flat number: several programs on the same computer can be waiting for
requests, and each listens on its own number.

Most addresses do not write the port, because it has a **default** value:

- 80 for `http`,
- 443 for `https`.

When it is not written, the client uses the default. Servers you try out on
your own computer usually run on a number such as `8000`:
`http://localhost:8000`.

## Path: which door

`/v1/weather` is the **path**. It says which endpoint of the API you are
going to; the **endpoint** from the previous section is exactly this.

There are two things you will often see in paths:

- **Version:** `/v1/`, `/v2/`. When an API changes, the new version opens on
  a new path so that old clients do not break; the old one keeps working for
  a while.
- **Identity:** `/books/42`. The last piece of the path points to a specific
  resource: book number 42. This is called a **path parameter**.

## Query string: extra details

`?city=Istanbul&units=metric` is the **query string**: extra details that
tell the server "what exactly, and how" you want.

- `?` marks the start of the query string; it appears **once** in an address.
- Each detail is written as `name=value`. These are called **query
  parameters**.
- Parameters are separated by `&`.

Their order does not matter: `?city=Istanbul&units=metric` and
`?units=metric&city=Istanbul` describe the same request. The same name can
appear more than once: `?tag=sea&tag=museum` means two tags.

One way to think about the difference between the path and the query string:
**the path says what** you want (`/books`), **the query string says how**
(`?author=Austen&sort=year`).

## Fragment: for the browser only

`#today` is the **fragment**. It tells the browser "scroll to this part of the
page". **It is never sent to the server.** It is useless in API requests; if
you see one, knowing that is enough.

## Special characters and percent-encoding

Some characters have a special meaning in the query string: `?` starts it,
`&` separates, `=` separates the name from the value. What if the value
itself contains these characters?

```text
?q=fish & chips
```

The server reads this as `q=fish ` and a meaningless ` chips`. The solution
is **percent-encoding**: the special character is written as `%` and a
two-digit code.

| Character | Encoded form |
|---|---|
| space | `%20` (`+` also works in the query string) |
| `&` | `%26` |
| `/` | `%2F` |
| `ı` | `%C4%B1` |
| `ö` | `%C3%B6` |

Letters outside English are encoded too: `Kadıköy` travels in the address as
`Kad%C4%B1k%C3%B6y`. You do not do this by hand; Python does it for you.

## URLs in Python: `urllib.parse`

Python's built-in `urllib.parse` module gives you everything you need to take
URLs apart and build them. Nothing to install.

### Taking it apart: `urlparse`

```python
from urllib.parse import urlparse

url = "https://api.example.com:8443/v1/weather?city=Istanbul&units=metric#today"
parts = urlparse(url)
print(parts.scheme)    # https
print(parts.hostname)  # api.example.com
print(parts.port)      # 8443
print(parts.path)      # /v1/weather
print(parts.query)     # city=Istanbul&units=metric
print(parts.fragment)  # today
```

If the address does not write a port, `parts.port` is `None`; it does not
fill in the default (443) for you.

### Reading the query string: `parse_qs`

```python
from urllib.parse import parse_qs

params = parse_qs("city=Istanbul&units=metric&tag=sea&tag=museum")
print(params)
# {'city': ['Istanbul'], 'units': ['metric'], 'tag': ['sea', 'museum']}
```

Careful: **every value is a list.** Because the same name can come more than
once, `parse_qs` puts even a single value into a list. To get the city you
write `params["city"][0]`.

### Building a query string: `urlencode`

```python
from urllib.parse import urlencode

query = urlencode({"city": "New York", "units": "metric", "days": 3})
print(query)   # city=New+York&units=metric&days=3
```

`urlencode` turns the space into `+`, turns the number into text and encodes
`&` and `=` for you. To build the address you add `?` in front:

```python
url = "https://api.example.com/v1/forecast?" + query
```

To send the same name several times, give a list with `doseq=True`:
`urlencode({"tag": ["sea", "museum"]}, doseq=True)` → `tag=sea&tag=museum`.

### Encoding a single value: `quote`

```python
from urllib.parse import quote, unquote

print(quote("fish & chips"))        # fish%20%26%20chips
print(quote("Kadıköy"))             # Kad%C4%B1k%C3%B6y
print(unquote("Kad%C4%B1k%C3%B6y")) # Kadıköy
```

`quote` is useful when you put a value inside the path: `/cities/` +
`quote(name)`.

## Joining the base address and the endpoint

API documentation usually gives a **base URL**: `https://api.example.com/v1`.
Endpoints are added after it. The most common mistake is the slash in
between:

```text
https://api.example.com/v1  +  weather   →  .../v1weather     (missing)
https://api.example.com/v1/ +  /weather  →  .../v1//weather   (one too many)
```

The safe way is to clean the slashes on both sides and join them with a
single slash:

```python
base = "https://api.example.com/v1/"
path = "/weather"
url = base.rstrip("/") + "/" + path.lstrip("/")
print(url)   # https://api.example.com/v1/weather
```

`rstrip("/")` removes slashes on the right, `lstrip("/")` on the left. In the
exercise you will turn this into a function.

## Common mistakes

- **Gluing the query string by hand.** Writing `"?q=" + text` breaks the
  address when the text contains a space or `&`. Use `urlencode`.
- **Writing `?` twice.** When adding parameters to an address, check whether
  it already has a `?`; further parameters come after `&`.
- **Thinking `#` reaches the server.** It does not.
- **Forgetting that a `parse_qs` value is a list.** `params["city"]` is a
  list, `params["city"][0]` is the value.

## Summary

- The parts of a URL: **scheme** (`https`), **host** (`api.example.com`),
  **port** (`:8443`, usually not written), **path** (`/v1/weather`), **query
  string** (`?city=Istanbul&units=metric`), **fragment** (`#today`).
- The path says **what** you want, the query string **how**. The fragment
  never reaches the server.
- `localhost` / `127.0.0.1` is your own computer.
- Special characters and non-English letters are written with
  **percent-encoding**.
- `urlparse` takes a URL apart, `parse_qs` reads the query (values are
  lists), `urlencode` builds a query, `quote` encodes a single value.
