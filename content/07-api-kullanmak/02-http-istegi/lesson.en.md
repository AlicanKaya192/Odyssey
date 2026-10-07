# The HTTP Request

You have learnt to build the address. But an address alone is not a request;
it is like the address on an envelope. What is inside the envelope, how it
should be opened and who it is from must be written too.

The client and the server write this information according to a shared rule
called **HTTP** (HyperText Transfer Protocol). A **protocol** is the set of
rules both sides follow when they talk: who speaks first, what is said in
which order. Your browser, your Python code and a server all speak the same
HTTP rules; that is why they understand each other.

In this section we open up an HTTP request and look at each of its parts.

## A request is really plain text

A weather request travels as text like this:

```text
GET /v1/weather?city=Istanbul HTTP/1.1
Host: api.example.com
Accept: application/json
User-Agent: odyssey-client/1.0

```

Do not be put off; it has four parts:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Request line</span><span><code>GET /v1/weather?city=Istanbul HTTP/1.1</code>: method, target, version</span></div>
    <div class="anat-row"><span>Headers</span><span><code>Host: ...</code>, <code>Accept: ...</code>: information about the request, one per line</span></div>
    <div class="anat-row"><span>Blank line</span><span>Says the headers have ended</span></div>
    <div class="anat-row"><span>Body</span><span>The data being sent; absent in a <code>GET</code> request</span></div>
  </div>
  <figcaption>Every HTTP request is made of these four parts. In this example the body is empty: nothing needs to be sent to read the weather.</figcaption>
</figure>

Now let's look at the parts one by one.

## The request line

The first line says three things, with a single space between them:

```text
GET  /v1/weather?city=Istanbul  HTTP/1.1
│    │                          │
│    target: path + query       HTTP version
method
```

- **Method:** what you want done. Here `GET`, "get it".
- **Target:** the path and query part of the URL. The scheme and host are
  not here; the host arrives shortly in the `Host` header.
- **Version:** `HTTP/1.1`. HTTP versions 2 and 3 exist too; they travel more
  efficiently but say the same things. It makes no difference on this path.

## Methods: what do you want to do?

HTTP has a handful of **methods**. Each tells the server to do a different
job:

| Method | Meaning | Example | Carries a body? |
|---|---|---|---|
| `GET` | Get it, read it | `GET /books/42` | No |
| `POST` | Create something new | `POST /books` | Yes |
| `PUT` | Replace it completely | `PUT /books/42` | Yes |
| `PATCH` | Change part of it | `PATCH /books/42` | Yes |
| `DELETE` | Delete it | `DELETE /books/42` | Usually no |

The same address does a completely different job with a different method:
`GET /books/42` fetches the book, `DELETE /books/42` deletes it. **The
address says what to touch, the method says what to do.**

The difference between `PUT` and `PATCH`: if you only want to change the
book's price, `PATCH` sends only the price. `PUT` replaces the **whole**
record with the new one; fields you leave out may be treated as removed.

Two more methods are worth recognising by name: `HEAD` (get only the
headers, not the body) and `OPTIONS` (which methods can be used at this
address?).

## Safe and idempotent methods

Two properties of methods will be very useful later, when handling errors:

- **Safe:** changes nothing on the server. `GET`, `HEAD`, `OPTIONS`. You can
  send them as often as you like.
- **Idempotent:** sending it once or ten times leaves the same result. In
  addition to the safe ones, `PUT` and `DELETE`. Deleting a book ten times is
  the same as deleting it once: the book is gone.

`POST` is neither. Send the "create a new order" request twice and you get
**two orders**. That is why, when the connection drops, you resend a `GET`
without a second thought, but think before resending a `POST`. We will use
this in Section 11.

## Headers: the details on the envelope

The lines after the request line are the **headers**. Each is written as
`Name: value`, one header per line:

```text
Host: api.example.com
Accept: application/json
User-Agent: odyssey-client/1.0
```

Headers are not the request itself but information **about** the request.
The ones you will meet most often:

| Header | What it says |
|---|---|
| `Host` | Which host the request goes to (required) |
| `Accept` | Which format you want the response in: `application/json` |
| `Content-Type` | The format of the body you are sending: `application/json` |
| `Content-Length` | How many bytes the body is |
| `Authorization` | Your identity: a key or a token (Section 08) |
| `User-Agent` | Which program sent the request |

Two rules:

- **Header names are not case-sensitive.** `Content-Type`, `content-type`
  and `CONTENT-TYPE` are the same header. That is why, inside a program, it
  is a good habit to lower-case header names before comparing them.
- A header's **name and value** are separated by the first `: ` (a colon and
  a space). The value may contain a colon too (`Host: localhost:8000`), so
  you split only at the **first** colon.

## The blank line and the body

The headers end with a **blank line**. Everything after the blank line is the
**body**: the data you send to the server.

A `GET` request has no body; everything you want is in the address. When you
add a new book (`POST`), the book's details travel in the body:

```text
POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 37

{"title": "Emma", "author": "Austen"}
```

Two headers describe the body here: `Content-Type` says "the body is JSON"
and `Content-Length` says "the body is 37 bytes". The server uses that number
to know where the body ends. (You do not count it by hand; the request
library works it out for you.)

`Content-Length` counts **bytes**, not letters. English letters take one byte
each, but letters such as `ş` or `ö` take two bytes each in UTF-8. In Python
the byte count is `len(text.encode("utf-8"))`.

## Reading a request in Python

In real work you will not write the request text by hand; a library such as
`requests` writes it for you. But knowing how the text is built lets you see
what went wrong when you get an error. Taking a request apart is a few lines:

```python
raw = """GET /v1/weather?city=Istanbul HTTP/1.1
Host: api.example.com
Accept: application/json"""

lines = raw.split("\n")
method, target, version = lines[0].split(" ")

headers = {}
for line in lines[1:]:
    name, value = line.split(": ", 1)
    headers[name.lower()] = value

print(method)           # GET
print(target)           # /v1/weather?city=Istanbul
print(headers["host"])  # api.example.com
```

Thanks to the final `1`, `split(": ", 1)` splits only at the **first**
separator and leaves any colon inside the value alone. Because `name.lower()`
lower-cases the header names, `headers["host"]` works however the header was
written.

## Choosing the right method

An API's documentation states the method of every endpoint. But if you know
what the methods mean, you can guess most of them without reading:

| What you want to do | Request |
|---|---|
| List all books | `GET /books` |
| See book number 42 | `GET /books/42` |
| Add a new book | `POST /books` (the book in the body) |
| Change the book's price | `PATCH /books/42` (the price in the body) |
| Replace the whole book | `PUT /books/42` (the whole book in the body) |
| Delete the book | `DELETE /books/42` |

Notice that when you add a new book the address is `/books`, the **list**.
You do not know the book's number yet; the server gives the new record its
number.

## Summary

- HTTP is the shared talking rule (protocol) of the client and the server.
- A request has four parts: the **request line** (method, target, version),
  the **headers**, a **blank line**, the **body**.
- Methods: `GET` gets, `POST` creates, `PUT` replaces, `PATCH` changes part,
  `DELETE` deletes. The address decides what, the method decides what to do.
- A **safe** method changes nothing (`GET`). Resending an **idempotent**
  method does not change the result (`GET`, `PUT`, `DELETE`). `POST` is
  neither.
- Headers are `Name: value`; names are not case-sensitive. `Content-Type`
  gives the body's format, `Content-Length` its size in bytes.
- A `GET` request has no body; data you send goes in the body of
  `POST`/`PUT`/`PATCH`.
