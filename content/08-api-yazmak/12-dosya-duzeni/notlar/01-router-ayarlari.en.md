The most used settings of `APIRouter` and `include_router`.

## `APIRouter(...)`

| Setting | What it does |
|---|---|
| `prefix="/books"` | Added to the start of every address |
| `tags=["books"]` | A heading in `/docs` |
| `dependencies=[Depends(f)]` | Runs on every endpoint in the router |

## `app.include_router(router, ...)`

The same settings can be given here too, and they're added **on top** of the
router's own. The most common use is a version prefix:

```python
app.include_router(books.router, prefix="/v1")
```

We measured: with the router's own prefix `/books`, the address became
`/v1/books`, and `/books` is now `404`.

## Why a version prefix?

Applications use your API, and one day you need to change the answer's
format. To avoid breaking old clients, you open the new format at
`/v2/books`, while `/v1/books` keeps working as before for a while.

```python
app.include_router(books_v1.router, prefix="/v1")
app.include_router(books_v2.router, prefix="/v2")
```

## A router inside a router

A router can include another router too: `router.include_router(reviews.router)`.
In big projects, sub-resources like `/books/{id}/reviews` are split out this
way.

## Writing addresses

| Router prefix | Endpoint | Real address |
|---|---|---|
| `/books` | `""` | `/books` |
| `/books` | `"/{book_id}"` | `/books/{book_id}` |
| `/books` | `"/"` | `/books/` (trailing slash) |

Don't mix up the first and the third: if you write `"/"`, the list address
becomes `/books/` and a request to `/books` gets redirected.
