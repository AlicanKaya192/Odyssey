# Overall Review

You have reached the end of the Using APIs module. You started with the question "what is an
API?"; now you can pull data from an API page by page, resilient to errors and
rate limits, and pour it into a clean dataset. This section walks the path
once more from start to finish: the most important idea and the code you will
use most at every stop.

<figure class="fig">
  <div class="flow">
    <span class="node">Basics<br><small>00–05</small></span><span class="arrow">→</span>
    <span class="node">requests<br><small>06–09</small></span><span class="arrow">→</span>
    <span class="node">Resilience<br><small>10–12</small></span><span class="arrow">→</span>
    <span class="node">REST<br><small>13–14</small></span><span class="arrow">→</span>
    <span class="node acc">Pipeline<br><small>15</small></span>
  </div>
  <figcaption>The path of the Using APIs module: from the concepts to a program that reliably pulls a real dataset.</figcaption>
</figure>

## 1. Concepts (Section 00)

An API is a door one program opens to other programs. The one asking is the
**client**, the one answering the **server**; every conversation is one
**request** and one **response**. An endpoint is a single door of the API; the
documentation is its menu.

## 2. The address (Section 01)

```text
https://api.example.com:8443/v1/books/42?author=Austen#notes
scheme   host            port path        query string  fragment
```

The path says **what** you want, the query string **how**; the fragment never
reaches the server. `localhost` is your own computer.

## 3. Request and response (Sections 02–03)

A request: the request line (method, target, version) + headers + a blank
line + the body. A response: the status line + headers + a blank line + the
body.

| Code | Meaning | What to do |
|---|---|---|
| `2xx` | Success | Use the body |
| `4xx` | Your mistake | Fix the request (except `429`) |
| `429` | Too often | Wait for `Retry-After` |
| `5xx` | The server's problem | Wait and try again |

## 4. JSON and tables (Sections 04–05)

`json.loads` goes from text to Python, `json.dumps` the other way. The five
steps of turning a nested response into a table: open the envelope, pick the
columns, flatten the nesting, decide about lists, fix the types.

## 5. requests (Sections 06–09)

```python
import requests

r = requests.get(url, params={...}, headers={...}, timeout=10)
r.status_code, r.headers["Content-Type"], r.json(), r.url
r.raise_for_status()

requests.post(url, json=data, headers=AUTH)        # 201 + Location
requests.patch(url, json={"price": 8.99}, headers=AUTH)
requests.delete(url, headers=AUTH)                 # 204
```

Identity: an `X-API-Key` header, `Authorization: Bearer <token>` or
`auth=(name, password)`. `401` not recognised, `403` not allowed. The key goes
in an environment variable, not the code.

## 6. Resilience (Sections 10–12)

- **Pagination:** page number, `next` link, offset + limit, cursor. The loop
  needs a clear stopping condition and a safety limit.
- **Errors:** a `timeout` on every request; catch `Timeout` and
  `ConnectionError`; retry only temporary errors and idempotent requests;
  exponential backoff.
- **Rate limits:** wait on `429`; better still, space out the requests.

## 7. Design and tools (Sections 13–14)

REST: resources and their addresses, nouns in the address / actions in the
method, the method and code contract, statelessness, links. Tools: the
browser and the Network tab, curl, Swagger UI / OpenAPI, Postman, Bruno.

## 8. The data pipeline (Section 15)

**Fetch → store → flatten → check → write.** Cache the raw response, check
before writing, update incrementally, and make sure the pipeline gives the
same result when run twice.

## All the pieces together

This short program uses almost every idea of the path:

```python
import os
import time
import requests

BASE = "http://api.odyssey.test"
token = os.environ.get("LIBRARY_TOKEN", "letmein")
session = requests.Session()
session.headers.update({"Authorization": "Bearer " + token})

def get(path, params=None):
    for attempt in range(4):
        try:
            r = session.get(BASE + path, params=params, timeout=10)
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 1)))
            continue
        if r.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("giving up on " + path)

books, url_params = [], {"tag": "scifi", "per_page": 20, "page": 1}
while True:
    body = get("/books", url_params)
    books.extend(body["data"])
    if not body["links"]["next"]:
        break
    url_params["page"] += 1
print(len(books), "science fiction books")
```

If you can read it line by line, this path has done its job.

## What comes next?

In the Writing APIs module you move to the other side of the table: you will write **your own**
API with FastAPI, define endpoints, validate incoming data, require identity
and see your documentation at `/docs`. Every rule you learnt here as a client
(methods, codes, REST design) is a rule you will apply there as a server.
