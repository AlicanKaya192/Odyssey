# Docs and Tools

Others will use your API: a mobile app, a web page, another team. They need
to understand it **without reading the code**. FastAPI produces the docs
from the code by itself; in this section you enrich them and see a few tools
that prepare the API for the outside world (CORS, middleware).

## Where do the docs come from?

Every endpoint, model and rule you write is turned into a standard document
called **OpenAPI**. It lives at three addresses (we measured, all `200`):

| Address | What? |
|---|---|
| `/openapi.json` | The document itself: JSON for machines to read |
| `/docs` | Swagger UI: a page with try-it buttons |
| `/redoc` | ReDoc: a tidy page for reading |

Since `/openapi.json` is a standard, other tools can read it too: tools that
generate client code, testing tools, API catalogues.

## The application's identity

```python
app = FastAPI(
    title="Library API",
    version="1.2.0",
    description="Books and authors of a small library.",
)
```

In `/openapi.json`:

```text
"openapi": "3.1.0"
"info": {"title": "Library API", "description": "Books and authors of a small library.",
         "version": "1.2.0"}
```

These appear in the `/docs` page's heading too. `version` is your API's
version; you raise it as you make changes.

## Describing an endpoint

```python
@app.get("/books/{book_id}", tags=["books"], summary="Read one book",
         responses={404: {"description": "No book with this id"}})
def read_book(book_id: int):
    """Returns the book with the given id.

    The id is the number given when the book was added.
    """
    ...
```

| Code | In the docs |
|---|---|
| `tags=["books"]` | Under the "books" heading |
| `summary="..."` | The endpoint's short name |
| The function's docstring | The long description (measured: it became `description` as it is) |
| `responses={404: {...}}` | `404` added to the list of possible error answers |

Without `summary`, FastAPI makes one from the function's name: `add_book` →
`"Add Book"`. Not bad, but "Read one book" is clearer.

Without `responses`, the docs show only `200` and FastAPI's own `422`; your
`HTTPException(404)` doesn't appear, because FastAPI can't know about it
without running your code. We measured: with `responses` the list is
`200, 404, 422`.

<figure class="fig">
  <div class="flow">
    <span class="node">Code<br><small>tags, summary, docstring, models</small></span><span class="arrow">→</span>
    <span class="node acc">/openapi.json</span><span class="arrow">→</span>
    <span class="node ok">/docs · /redoc<br><small>client generators</small></span>
  </div>
  <figcaption>You don't write the docs separately: every piece of information you add to the code becomes a standard document that pages and tools read.</figcaption>
</figure>

## An example for the model

```python
class Book(BaseModel):
    title: str = Field(examples=["Dune"])
    year: int = Field(examples=[1965], description="Year of first publication")
```

The try-it button in `/docs` fills the body with `"Dune"` and `1965` instead
of `"string"` and `0`; the description is written next to the field.

## Ageing and hidden endpoints

```python
@app.get("/old-books", deprecated=True)
def old_books():
    ...


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
```

- `deprecated=True`: the endpoint works but appears **struck through** in the
  docs; it means "don't use this, it's going away soon".
- `include_in_schema=False`: the endpoint works (`/health` → `200`) but isn't
  in the docs at all. For internal addresses used by tools that watch the
  server.

## When called from a browser: CORS

When a web page (`https://library.example.com`) sends a request to your API
(`https://api.example.com`) from the browser, the browser first asks: "does
this API allow being called from another site?" Permission is given with an
`Access-Control-Allow-Origin` header in the answer. This is called **CORS**.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://library.example.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

We measured:

```text
GET, Origin: https://library.example.com
    200  access-control-allow-origin: https://library.example.com
GET, Origin: https://evil.example.com
    200  (no permission header)
OPTIONS preflight, library.example.com
    200  access-control-allow-methods: GET, POST
OPTIONS preflight, evil.example.com
    400  Disallowed CORS origin
```

Note the second line: the request **still returned `200`**. CORS doesn't
protect the server; it tells the browser "don't show this answer to that
page". `requests` or `curl` never look at CORS. The real protection is what
you saw in the Authentication section.

`allow_origins=["*"]` allows everyone; don't use it on APIs that carry
credentials, write the allowed sites one by one.

## Touching every request: middleware

Middleware is code that runs in front of and behind **every** request:

```python
import time
from fastapi import Request


@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response
```

`call_next(request)` passes the request on to the endpoint and brings back
the answer; before and after are yours. We measured: `x-process-time: 0.0013`
in the answer. It's used for writing logs, measuring time, adding a shared
header to every answer.

## Running the server

In Odyssey the **Start server** button does this for you. On your own
computer:

```text
uvicorn main:app --reload
```

`main:app`: the `app` variable in the `main.py` file. `--reload`: the server
restarts whenever you save the code; only while developing. The default
address is `http://127.0.0.1:8000`; the docs are at
`http://127.0.0.1:8000/docs`.

## Summary

- The docs are made from the code: `/openapi.json`, `/docs`, `/redoc`.
- `FastAPI(title=, version=, description=)`; on endpoints `tags`, `summary`,
  the docstring, `responses`.
- `Field(examples=[...], description=...)` fills the try-it button.
- `deprecated=True` is struck through, `include_in_schema=False` is hidden.
- CORS is for browsers and doesn't protect the server; list allowed sites
  one by one.
- `@app.middleware("http")`: runs in front of and behind every request.
