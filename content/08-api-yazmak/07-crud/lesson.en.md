# CRUD: A Complete Resource

Until now you wrote the parts one by one: path, query, body, validation,
response model, status codes. In this section you put them all together
and write **a complete resource**: adding, listing, reading, changing and
deleting books. These five jobs are called **CRUD** for short.

## CRUD and HTTP methods

| Job | Letter | Method | Address | Success code |
|---|---|---|---|---|
| Create | **C** | `POST` | `/books` | `201` |
| List | **R**ead | `GET` | `/books` | `200` |
| Read one | **R**ead | `GET` | `/books/{id}` | `200` |
| Replace all of it | **U**pdate | `PUT` | `/books/{id}` | `200` |
| Change part of it | **U**pdate | `PATCH` | `/books/{id}` | `200` |
| Delete | **D** | `DELETE` | `/books/{id}` | `204` |

Two addresses are enough: the collection (`/books`) and one record
(`/books/{id}`). The method says what to do. This is the pattern you used
as a client in the Using APIs module; now you're writing its server.

<figure class="fig">
  <div class="versus">
    <div><h4>/books (the collection)</h4><p><code>POST</code> → a new book, <code>201</code><br><code>GET</code> → the list, <code>200</code></p></div>
    <div><h4>/books/{id} (one record)</h4><p><code>GET</code> → the book or <code>404</code><br><code>PUT</code> / <code>PATCH</code> → change<br><code>DELETE</code> → delete, <code>204</code></p></div>
  </div>
  <figcaption>Two addresses, five methods. The address says what is worked on, the method says what is done.</figcaption>
</figure>

## The models

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1


class BookIn(BaseModel):
    title: str = Field(min_length=1)
    year: int


class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    year: int | None = None


class BookOut(BookIn):
    id: int
```

- `BookIn`: the body when creating and in `PUT`; both fields required.
- `BookPatch`: the `PATCH` body; **every field optional**, because people
  send only what they want to change.
- `BookOut`: the answer; `BookIn`'s fields + `id`.

## The id number: the `len()` trap

The first idea is `new_id = len(books) + 1`. We measured:

```text
POST /books  A      201 {"id": 1}
POST /books  B      201 {"id": 2}
DELETE /books/1     204
POST /books  C      201 {"id": 2}     ← B's number!
GET /books          {"2": C}          ← B is gone
```

After a deletion the number of records drops and the new record is written
over an existing one. The fix: a counter that never goes back.

```python
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookIn) -> BookOut:
    global next_id
    record = {"id": next_id, **book.model_dump()}
    books[next_id] = record
    next_id += 1
    return record
```

`global next_id`: says we will **change** the module's `next_id` inside the
function; without it Python takes it for the function's own variable and
raises `UnboundLocalError`. (In the database section the database will do
this job.)

## 404 if not found: a shared helper

Reading, changing and deleting all have to find the record first. To avoid
writing the same `if` three times:

```python
def find_book(book_id: int) -> dict:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
```

`raise HTTPException(...)` stops the function there and sends the error
answer; it works even when raised from inside the helper. Details in the
next section.

## Reading and listing

```python
@app.get("/books")
def list_books(year: int | None = None) -> list[BookOut]:
    result = list(books.values())
    if year is not None:
        result = [b for b in result if b["year"] == year]
    return result


@app.get("/books/{book_id}")
def read_book(book_id: int) -> BookOut:
    return find_book(book_id)
```

The list takes an optional filter: `GET /books?year=1815`.

## `PUT`: replace all of it

```python
@app.put("/books/{book_id}")
def replace_book(book_id: int, book: BookIn) -> BookOut:
    find_book(book_id)
    books[book_id] = {"id": book_id, **book.model_dump()}
    return books[book_id]
```

`PUT` replaces the **whole** record with what was sent; that's why it takes
`BookIn` and a missing field is `422`:

```text
PUT /books/2  {"title": "Persuasion", "year": 1817}   200
PUT /books/2  {"title": "Persuasion"}                 422 missing year
```

## `PATCH`: change only what was sent

```python
@app.patch("/books/{book_id}")
def update_book(book_id: int, patch: BookPatch) -> BookOut:
    record = find_book(book_id)
    record.update(patch.model_dump(exclude_unset=True))
    return record
```

The trick is `exclude_unset=True`. When `{"year": 1966}` is sent:

```text
patch.model_dump()                    {"title": None, "year": 1966}
patch.model_dump(exclude_unset=True)  {"year": 1966}
```

Without `exclude_unset` the title would turn into `None`. This option gives
the fields the client **sent**; it tells "not sent" apart from "sent as
`null` on purpose".

### A `null` that was sent

While measuring we caught a bug: `PATCH /books/1 {"title": null}` →
**`500`**. `BookPatch` accepts `null` (`str | None`), the record gets
`title: None`, and then the response model `BookOut` (`title: str`) rejects
it. The record stays broken too. The fix: reject a `null` sent in a `PATCH`
right away:

```python
class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    year: int | None = None

    @field_validator("title", "year")
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("may not be null")
        return value
```

The validator runs only on fields that were **sent** (the default `None`
isn't checked). Now `{"title": null}` → `422`, while `{}` and
`{"year": 1966}` → `200`.

## Deleting

```python
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    find_book(book_id)
    del books[book_id]
```

## The whole flow (measured)

```text
POST   /books      {"title": "Dune", "year": 1965}  201 {"title":"Dune","year":1965,"id":1}
POST   /books      Emma, Ubik                       201 id 2, 3
GET    /books?year=1815                             200 [{"title":"Emma",...,"id":2}]
GET    /books/9                                     404 {"detail":"Book not found"}
PATCH  /books/1    {"year": 1966}                   200 {"title":"Dune","year":1966,"id":1}
DELETE /books/3                                     204
DELETE /books/3                                     404
POST   /books      {"title": "Kindred", ...}        201 ... "id":4
```

The last line matters: 3 was deleted but the new book got `4`; a number
never repeats. The field order in the answer is `title, year, id` because
`BookOut` inherits from `BookIn` and the base model's fields come first.

## Summary

- Two addresses (`/books`, `/books/{id}`) + five methods = CRUD.
- A counter that never goes back for ids; `len() + 1` overwrites records
  after a deletion.
- A shared "find or 404" helper.
- `PUT` replaces everything (`BookIn`), `PATCH` changes what was sent
  (`BookPatch` + `exclude_unset=True`).
- Creating `201`, deleting `204`, not found `404`.
