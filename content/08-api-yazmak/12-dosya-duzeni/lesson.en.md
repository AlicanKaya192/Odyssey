# Project Layout: Routers

Until now the whole API lived in one `main.py`. Books, users, an admin page,
models, dependencies... At some point the file reaches hundreds of lines
and you can't find what you're looking for. In this section you split the
API into **files**.

## The target layout

```text
main.py            the application: brings the routers together
models.py          Pydantic models
deps.py            shared dependencies (key, database)
routers/
    __init__.py    empty: says "this folder is a package"
    books.py       the /books endpoints
    admin.py       the /admin endpoints
```

Remember the modules section of the Python track: every `.py` file is a
module, used from another file with `import`. The `__init__.py` inside the
`routers/` folder makes it a **package**, so you can write
`from routers import books`.

## `APIRouter`: a small `app`

`routers/books.py`:

```python
from fastapi import APIRouter, HTTPException

from models import Book

router = APIRouter(prefix="/books", tags=["books"])
books = {1: {"title": "Dune", "year": 1965}}


@router.get("")
def list_books():
    return books


@router.get("/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@router.post("", status_code=201)
def add_book(book: Book):
    ...
```

- `APIRouter` gathers endpoints like `app` does, but doesn't run on its own;
  it has to be **added** to an application.
- `prefix="/books"`: added to the start of every address in this file.
  `@router.get("/{book_id}")` is really `/books/{book_id}`.
- `@router.get("")`: just the prefix, i.e. `/books`.
- `tags=["books"]`: in `/docs` these endpoints are grouped under a "books"
  heading.

## `main.py`: bringing them together

```python
from fastapi import FastAPI

from routers import admin, books

app = FastAPI(title="Library")
app.include_router(books.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"name": "Library"}
```

`include_router` adds all of the router's endpoints to the application. We
measured:

```text
GET /books        200 {"1": {"title": "Dune", "year": 1965}}
GET /books/1      200 {"title": "Dune", "year": 1965}
GET /books/7      404 {"detail": "Book not found"}
POST /books       201 {"id": 2, "title": "Emma", "year": 1815}
GET /             200 {"name": "Library"}
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">main.py<br><small>app + include_router</small></span><span class="arrow">→</span>
    <span class="node">routers/books.py<br><small>prefix /books</small></span><span class="arrow">→</span>
    <span class="node">models.py · deps.py</span>
  </div>
  <figcaption>Imports go one way: <code>main</code> imports the routers, the routers import the models and dependencies. The other way creates a cycle.</figcaption>
</figure>

## A dependency for the whole router

Let **all** admin endpoints require the key. Instead of writing
`dependencies=` on each, put it on the router once:

```python
# deps.py
def require_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "letmein":
        raise HTTPException(status_code=401, detail="Invalid API key")
```

```python
# routers/admin.py
from fastapi import APIRouter, Depends

from deps import require_key

router = APIRouter(prefix="/admin", tags=["admin"],
                   dependencies=[Depends(require_key)])


@router.get("/stats")
def stats():
    return {"books": 1}
```

```text
GET /admin/stats                       401 {"detail": "Invalid API key"}
GET /admin/stats  (X-Api-Key: letmein) 200 {"books": 1}
```

Every new endpoint added to this router is protected automatically; there's
no chance of forgetting.

## The trailing slash

With the prefix `/books` and the endpoint `""`, the address is `/books`.
When `GET /books/` (with a trailing `/`) is sent, FastAPI redirects to
`/books` with `307` (we measured). Browsers and `requests` follow the
redirect by themselves, but a `POST` body can get lost on a redirect. Write
addresses exactly as they are in the docs.

## What goes where?

| File | Contains | Imports |
|---|---|---|
| `models.py` | Pydantic models | Only `pydantic` |
| `deps.py` | `get_db`, `require_key`, `current_user` | `fastapi`, the database |
| `routers/*.py` | Endpoints | `models`, `deps` |
| `main.py` | `app`, `include_router` | `routers` |

The arrow goes one way: `main` → `routers` → `models`, `deps`. If you write
an `import` the other way (for example `from main import app` in
`models.py`), you get a **circular import** and the program doesn't start.

## Summary

- `APIRouter(prefix=..., tags=...)` gathers a file's endpoints.
- `app.include_router(router)` adds them to the application.
- `dependencies=[...]` on a router: every endpoint in it is protected.
- `routers/__init__.py` makes the folder a package.
- Imports go one way: `main` → `routers` → `models`/`deps`.
