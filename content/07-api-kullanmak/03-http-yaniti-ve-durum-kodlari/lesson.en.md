# The HTTP Response and Status Codes

You sent the request. Whatever the server says, the answer comes back in the
same form: an **HTTP response**. The three-digit number on the first line of
the response is its most important piece of information: the **status
code**. It says whether the request worked, and if not, whose fault it was.

When working with an API, the first job with every response is to look at the
status code. Code that reads the body without first asking "did the request
succeed?" will one day take an error message for data and produce a wrong
result.

## A response is plain text too

The response to the weather request looks like this on the way back:

```text
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 49

{"city": "Istanbul", "temp": 18, "sky": "cloudy"}
```

The structure is very much like a request:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Status line</span><span><code>HTTP/1.1 200 OK</code>: version, status code, reason</span></div>
    <div class="anat-row"><span>Headers</span><span><code>Content-Type</code>, <code>Content-Length</code>: information about the response</span></div>
    <div class="anat-row"><span>Blank line</span><span>Says the headers have ended</span></div>
    <div class="anat-row"><span>Body</span><span>The actual data, or an explanation of the error</span></div>
  </div>
  <figcaption>The same four parts as a request; only the first line differs. The request says "what I want", the response "what happened".</figcaption>
</figure>

The only difference is the first line: the request had a **request line**
(method, target, version), the response has a **status line**.

## The status line

```text
HTTP/1.1  200  OK
│         │    │
version   code reason
```

- **Version:** the same as the request's.
- **Code:** a three-digit number. This is what your program looks at.
- **Reason phrase:** the code's name written for people. It can differ
  between servers and is not sent at all in HTTP/2. **In your program, look
  at the code, not the phrase.**

## The first digit says it all

The first digit of the status code is a **class**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>1xx</span><span>Information: "carry on". You rarely see these.</span></div>
    <div class="anat-row"><span>2xx</span><span><b>Success.</b> The request was carried out.</span></div>
    <div class="anat-row"><span>3xx</span><span>Redirect: what you want is at another address.</span></div>
    <div class="anat-row"><span>4xx</span><span><b>Client error:</b> something is wrong with your request.</span></div>
    <div class="anat-row"><span>5xx</span><span><b>Server error:</b> the request may be fine; the server has a problem.</span></div>
  </div>
  <figcaption>The first digit of the code gives the class. Even if you had never seen 404, it starts with 4, so you know "my request has a problem".</figcaption>
</figure>

The most useful distinction is between 4 and 5:

- **4xx:** "You asked for something wrong." Wrong address, missing key,
  broken body. Send the same request again unchanged and you get the same
  error; you need to **fix the request**.
- **5xx:** "I have a problem." The server crashed, is under maintenance or
  overloaded. The request may be fine; **waiting a while and trying again**
  may work.

In Python, integer division is enough to get the first digit: `404 // 100` →
`4`.

## Codes you will see often

| Code | Name | When |
|---|---|---|
| `200` | OK | The request succeeded; the response is in the body |
| `201` | Created | A new record was created with `POST` |
| `204` | No Content | Success, but the body is empty (often `DELETE`) |
| `301` | Moved Permanently | The resource has permanently moved to another address |
| `304` | Not Modified | The copy you have is still up to date |
| `400` | Bad Request | The request is broken: missing or malformed information |
| `401` | Unauthorized | You did not say who you are, or the key is invalid |
| `403` | Forbidden | I know who you are, but you are not allowed to do this |
| `404` | Not Found | No such address or record |
| `405` | Method Not Allowed | This method cannot be used at this address |
| `409` | Conflict | Clashes with the resource's current state (the name already exists) |
| `422` | Unprocessable Content | The format is right but the values are invalid (age −5) |
| `429` | Too Many Requests | You sent requests too often; wait a little |
| `500` | Internal Server Error | An error happened in the server's code |
| `502` | Bad Gateway | The server in between got a broken response from the one behind it |
| `503` | Service Unavailable | The server cannot serve right now (maintenance, load) |
| `504` | Gateway Timeout | The server in between got no timely response from the one behind it |

You do not need to memorise these. Always know the class (the first digit);
for the details, look at this table or the API's documentation when needed.

## Commonly confused pairs

**401 and 403.** Their names are misleading. `401` means "I don't know you":
no key or a wrong one. `403` means "I know you, but this door is closed to
you". With 401 you check your key; with 403 you need another key or
permission.

**400 and 422.** With `400` the request itself cannot be read (like broken
JSON). With `422` it can be read but the values inside break the rules (an
empty title, a negative price). Some APIs use `400` for both.

**404 does not always mean "wrong address".** `/books/9999` may be written
correctly; there is just no book number 9999. The server says `404` in both
cases.

## Response headers

As in requests, headers in a response carry information **about** the
response:

| Header | What it says |
|---|---|
| `Content-Type` | The body's format: `application/json; charset=utf-8` |
| `Content-Length` | The body's size in bytes |
| `Location` | With `201`, the new record's address; with `3xx`, the new address to go to |
| `Retry-After` | With `429` and `503`: after how many seconds you may try again |

A `Content-Type` value may end with something like `; charset=utf-8`; it says
which encoding the text is written in. When you ask about the format, look at
the part before the semicolon.

## The body of error responses

A good API says why when it returns an error:

```text
HTTP/1.1 422 Unprocessable Content
Content-Type: application/json

{"error": "validation", "detail": "price must be positive"}
```

The status code answers "what kind of problem", the body answers "exactly
what". When you get an error, reading the body often tells you the fix
directly.

## What to do when

| You get | What to do |
|---|---|
| `2xx` | Use the body (`204` has no body) |
| `3xx` | Go to the address in `Location` (request libraries do this for you) |
| `401` / `403` | Check your key and your permissions |
| `404` | Check the address and the record's identifier |
| `429` | Wait for `Retry-After`, then try again |
| Other `4xx` | Fix the request; do not resend the same one |
| `5xx` | Wait a while and try again; if it continues, tell the server's owner |

This table is the skeleton of the error handling you will write in Section 11.

## Status codes in Python

Python's built-in `http` module has the names of all codes:

```python
from http import HTTPStatus

print(HTTPStatus(404).phrase)   # Not Found
print(HTTPStatus(429).phrase)   # Too Many Requests
print(HTTPStatus.OK.value)      # 200
```

Sorting a code into its class:

```python
code = 503
kind = code // 100
if kind == 2:
    print("success")
elif kind == 4:
    print("my request is wrong")
elif kind == 5:
    print("the server has a problem")
```

## Summary

- A response has four parts: the **status line** (version, code, reason),
  the **headers**, a **blank line**, the **body**.
- In a program, look at the **code**, not the reason phrase.
- The first digit gives the class: `2xx` success, `3xx` redirect, `4xx` your
  mistake, `5xx` the server's problem.
- With `4xx`, fix the request; with `5xx` and `429`, wait and try again.
- `401` you are not recognised, `403` not allowed, `404` no such thing, `422`
  invalid values.
- The body of an error response often says why; read it.
