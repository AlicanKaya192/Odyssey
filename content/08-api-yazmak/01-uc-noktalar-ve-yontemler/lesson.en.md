# Endpoints and Methods

In the first section you wrote a single `GET` endpoint. In a real API the
same address is reached with different methods: `GET /counter` **reads** the
counter, `POST /counter` **increases** it. In this section you see the
methods, the application's memory and how FastAPI turns the values you
return into JSON.

## One decorator per method

Every HTTP method you learned in API 1 has a decorator in FastAPI:

| Method | Decorator | Usually for? |
|---|---|---|
| `GET` | `@app.get("/path")` | Reading |
| `POST` | `@app.post("/path")` | Creating something new, starting an action |
| `PUT` | `@app.put("/path")` | Replacing a whole record |
| `PATCH` | `@app.patch("/path")` | Changing part of a record |
| `DELETE` | `@app.delete("/path")` | Deleting |

Separate functions can be connected to the same address with different
methods. FastAPI looks at the request's **method and address together** and
picks the right function:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>GET /counter</span><span><code>read_counter()</code> → reads the counter</span></div>
    <div class="anat-row"><span>POST /counter</span><span><code>increase()</code> → increases the counter</span></div>
    <div class="anat-row"><span>DELETE /counter</span><span>no function → <code>405 Method Not Allowed</code></span></div>
    <div class="anat-row"><span>GET /countr</span><span>no address → <code>404 Not Found</code></span></div>
  </div>
  <figcaption>FastAPI matches the method and the address together. Same address, different method: a different function.</figcaption>
</figure>

## The application's memory

Let us write a counter that can be read and increased.

```python
from fastapi import FastAPI

app = FastAPI()
state = {"count": 0}


@app.get("/counter")
def read_counter():
    return state


@app.post("/counter")
def increase():
    state["count"] += 1
    return state
```

`state` is defined **outside** the functions, at the top of the file: it
stays in memory as long as the server is running, and every request sees
the same dictionary. If we defined it inside the function, it would start
from `0` on every request.

Changing the inside of a dictionary (`state["count"] += 1`) can be done
directly from inside a function. That is why we keep the number in a
dictionary rather than a plain variable (`count = 0`); changing a plain
variable from inside a function needs an extra rule (`global`).

Requests sent in order and their answers (measured):

```text
GET  /counter   200  {"count":0}
POST /counter   200  {"count":1}
POST /counter   200  {"count":2}
GET  /counter   200  {"count":2}
```

**Watch out:** this memory is temporary. When the server stops (or
`--reload` restarts it), the counter goes back to `0`. Permanent data needs
a database; we will do that in the Database section.

## The wrong method: 405

We did not write a `DELETE` for the counter. If someone sends one anyway:

```text
DELETE /counter   405  {"detail":"Method Not Allowed"}
```

`405`, not `404`: the address **exists**, but this method is not allowed. In
API 1 you learned to tell these two codes apart as a client; now FastAPI
gives them correctly for you.

## Whatever you return becomes JSON

An endpoint can return values other than dictionaries and lists; FastAPI
turns all of them into JSON (measured):

| What the function returns | The body that comes back |
|---|---|
| `{"count": 2}` | `{"count":2}` |
| `["red", "green"]` | `["red","green"]` |
| `3.14159` | `3.14159` |
| `"Odyssey"` | `"Odyssey"` (with quotes: a JSON string) |
| `None` | `null` |

All with `content-type: application/json` and `200`. We will see how to
change the status code in the Response Models and Status Codes section.

## The trailing slash

You wrote `@app.get("/books")` but the client asked for `/books/`. FastAPI
redirects the client to `/books` with `307 Temporary Redirect` (measured);
browsers and `requests` follow the redirect by themselves. Still, write
addresses consistently: **without** a slash at the end (`/books`,
`/books/42`).

## Good address, good method

The REST rules from API 1 are your responsibility here:

- The address names a **thing** (a resource), the method says **what to
  do**: `POST /counter`, not `POST /increase-counter`.
- Lowercase and plural names in addresses: `/books`, `/users`.
- `GET` should change nothing. A browser or a cache may repeat a `GET` as
  often as it likes; if `GET` increased the counter, everyone who refreshed
  the page would increase it.

## Summary

- Every method has a decorator: `get`, `post`, `put`, `patch`, `delete`.
  Different functions are connected to the same address with different
  methods.
- Data defined outside the functions lives as long as the server runs; it
  is lost when the server stops.
- The address exists but not the method: `405`; no address: `404`.
- Every returned value becomes JSON: dictionary, list, number, string,
  `None` → `null`.
- `GET` only reads; changing things uses other methods.
