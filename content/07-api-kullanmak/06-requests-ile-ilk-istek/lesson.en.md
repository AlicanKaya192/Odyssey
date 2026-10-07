# Your First Request with requests

So far you have studied requests and responses on paper, as text. In this
section you send a **real request** for the first time: your Python code will
connect to a server, write the HTTP request, wait for the response and read
it.

For this we use the most widely used library in the Python world:
**requests**. Its one job is sending HTTP requests and making that as easy as
possible.

## The practice server

Sending requests to a real API needs the internet, sometimes an account,
sometimes money, and the results change every day. That is why the exercises
on this path send requests to a **practice server that runs inside Odyssey**:

```text
http://api.odyssey.test
```

It is a library API: books, authors, filtering, pagination,
authentication... It behaves like a real server; your request really travels
through a socket and the status codes really come back. The only difference
is that the request **never leaves your computer**. The `.test` ending
belongs to no site in the world; Odyssey routes this name to the server
inside it.

When you run an exercise, the terminal also shows the requests that reached
the server:

```text
Requests sent to the practice server (1):
  → GET /books/1  200
```

## Installing requests

requests does not come with Python; it is a separate package. To use it in a
project on your own computer:

```text
python -m pip install requests
```

It comes installed in Odyssey's exercise environment; there is nothing to do
here. You saw how to install packages in the "Packages and Environments"
section of the Python path.

## The first request: `requests.get`

```python
import requests

response = requests.get("http://api.odyssey.test/books/1")
print(response.status_code)   # 200
```

What happens in these two lines is everything you learnt piece by piece in
the previous sections:

<figure class="fig">
  <div class="flow">
    <span class="node">requests.get(...)</span><span class="arrow">→</span>
    <span class="node">HTTP request<br><small>GET /books/1</small></span><span class="arrow">→</span>
    <span class="node acc">Server</span><span class="arrow">→</span>
    <span class="node">HTTP response<br><small>200 + JSON</small></span><span class="arrow">→</span>
    <span class="node">Response object</span>
  </div>
  <figcaption>requests builds the request line and headers and parses the response; all that is left to you is the address and the result.</figcaption>
</figure>

`requests.get` sends a `GET` request and waits until the response arrives.
The value it returns is a **response object** (`Response`): everything the
server said is inside it.

## The parts of the response object

```python
print(response.status_code)               # 200
print(response.ok)                        # True
print(response.headers["Content-Type"])   # application/json; charset=utf-8
print(response.url)                       # http://api.odyssey.test/books/1
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>status_code</code></span><span>The status code: <code>200</code>, <code>404</code>...</span></div>
    <div class="anat-row"><span><code>ok</code></span><span><code>True</code> when the code is below 400</span></div>
    <div class="anat-row"><span><code>headers</code></span><span>The response headers; names are not case-sensitive</span></div>
    <div class="anat-row"><span><code>text</code></span><span>The body as text</span></div>
    <div class="anat-row"><span><code>json()</code></span><span>The body as a Python object</span></div>
    <div class="anat-row"><span><code>url</code></span><span>The final address the request went to</span></div>
    <div class="anat-row"><span><code>request</code></span><span>The request that produced this response (method, address, headers)</span></div>
  </div>
  <figcaption>The response you read piece by piece in Section 03 is the fields of an object in requests.</figcaption>
</figure>

`response.ok` is `True` when the status code is below 400. It is handy for a
quick "is something wrong?", but it does not say which problem; for details
you look at `status_code`.

`response.headers` works like a dictionary and, as you learnt in Section 02,
**names are not case-sensitive**: `response.headers["content-type"]` gives
the same value.

## Reading the body: `text` and `json()`

You can get the body in two forms:

- `response.text`: the body as **text**. It may be JSON text or plain
  writing.
- `response.json()`: parses the body as JSON and returns a **Python
  object**. The same job as `json.loads(response.text)` from Section 04.

```python
book = response.json()
print(book["title"], book["author"]["name"])   # Emma Austen
```

`json()` is a method (it ends with brackets), `text` is an attribute (no
brackets). Mixing them up is a common mistake.

If the body is not JSON, `json()` raises an error:

```python
r = requests.get("http://api.odyssey.test/status")
print(r.headers["Content-Type"])   # text/plain; charset=utf-8
print(r.text)                      # ok
r.json()   # requests.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

So when you are not sure, look at `Content-Type` first: if it starts with
`application/json` use `json()`, otherwise `text`.

## Status code first, body second

Let's ask for a book that does not exist:

```python
r = requests.get("http://api.odyssey.test/books/99")
print(r.status_code, r.ok)   # 404 False
print(r.json())              # {'error': 'book not found', 'id': 99}
```

**requests does not raise an error because a 404 came back.** A response
arrived; looking at what it says is up to you. Code that writes
`r.json()["title"]` without looking at the status code fails here with a
`KeyError`, or worse, takes the error message for data and carries on. The
rule from Section 03 holds here too: **code first.**

```python
r = requests.get("http://api.odyssey.test/books/99")
if r.status_code == 200:
    print(r.json()["title"])
else:
    print("error", r.status_code)
```

## `raise_for_status`: turning an error code into an error

Instead of writing an `if` after every request, you can tell requests
"raise an exception if the code is an error":

```python
r = requests.get("http://api.odyssey.test/books/99")
try:
    r.raise_for_status()
except requests.HTTPError as error:
    print("HTTPError:", error)
# HTTPError: 404 Client Error: Not Found for url: http://api.odyssey.test/books/99
```

`raise_for_status()` raises `requests.HTTPError` if the code is 400 or above
and does nothing otherwise. Many programs call it right after the request: if
something went wrong, the program stops there and says why.

## The request is an object too

When debugging, the question "what did I actually send?" helps a lot. The
response also carries the request that produced it:

```python
print(response.request.method)    # GET
print(response.request.url)       # http://api.odyssey.test/books/1
print(response.request.headers)   # the headers requests added
```

requests adds headers such as `User-Agent` and `Accept` itself; it builds the
whole request you wrote by hand in Section 02 for you.

## Common mistakes

- **Forgetting the scheme.** `requests.get("api.odyssey.test/books")` raises
  `MissingSchema`. The address must start with `http://` or `https://`.
- **Mixing up `json` and `json()`.** `response.json` (no brackets) is the
  method itself; to get the data, `response.json()`.
- **Not looking at the status code.** 404 and 500 are "responses" too;
  requests does not count them as errors.
- **Parsing the body twice.** `json.loads(response.json())` fails; `json()`
  already returns a Python object.

## Summary

- `requests.get(address)` sends a `GET` request and returns a `Response`.
- The parts of the response: `status_code`, `ok`, `headers`, `text`, `json()`,
  `url`, `request`.
- `text` is the body's text, `json()` the parsed Python object. If it is not
  JSON, `json()` fails; check `Content-Type` first.
- requests does not raise on 4xx/5xx responses; either look at the status code
  or turn it into an error with `raise_for_status()`.
- The exercises go to the practice server at `http://api.odyssey.test`; the
  request never leaves your computer.
