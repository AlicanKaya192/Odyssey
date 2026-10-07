# Request Bodies and Pydantic

Until now all the information came in the address: the path and the query.
When adding a new book, though, the title, year, tags, a note... do not fit
in the address, and should not. In API 1 you sent a **body** with
`requests.post(url, json={...})`. In this section you write the side that
receives the body, and you describe the body's shape with **Pydantic**.

## The body's template: a model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    year: int
```

`Book` is a **model**: a template that says which fields the incoming JSON
must contain and of which types. You wrote classes on the Python track;
here you only list the fields and their types, `BaseModel` does the rest.

When a parameter's type in the endpoint is this model, FastAPI reads the
value from the **body**:

```python
books = []


@app.post("/books", status_code=201)
def add_book(book: Book):
    books.append(book)
    return {"id": len(books), **book.model_dump()}
```

- `book: Book`: the body must fit the `Book` template.
- `book.title`, `book.year`: fields are reached with a dot.
- `book.model_dump()`: turns the model into a dictionary; `**` unpacks it
  into another dictionary.
- `status_code=201`: the "created" code. Details in the Response Models and
  Status Codes section.

<figure class="fig">
  <div class="flow">
    <span class="node">Body (JSON)<br><small>{"title": "Dune", "year": "1965"}</small></span><span class="arrow">→</span>
    <span class="node acc">Book model<br><small>title: str, year: int</small></span><span class="arrow">→</span>
    <span class="node ok">book object<br><small>book.year == 1965</small></span>
  </div>
  <figcaption>The body first passes through the model's template: fields are checked and those that can be converted are converted. If it does not fit, the function is never called and <code>422</code> goes back.</figcaption>
</figure>

## Checks for free

If the body does not fit the template, the function is not called; FastAPI
gives `422`. What we measured:

| Body sent | Result |
|---|---|
| `{"title": "Dune", "year": 1965}` | `201` |
| `{"title": "Dune"}` | `422` missing, `loc: ["body", "year"]` |
| `{"title": "Dune", "year": "nineteen"}` | `422` int_parsing |
| `{"title": 5, "year": 1965}` | `422` string_type |
| `{"title": "Dune", "year": 1965.5}` | `422` int_from_float |
| `{"title": "Dune", "year": "1965"}` | `201`: the text became a number |

Two things stand out:

- `"1965"` (quoted) was accepted: Pydantic converts text that can be turned
  into a number. But it does not turn `5` into text, nor `1965.5` into an
  integer; it rejects conversions that would lose information.
- `loc` now starts with `body`: it says which field of the body the error is
  in.

No body at all, or broken JSON, is `422` too:

```text
(no body)        422  type: missing, loc: ["body"]
{bad json        422  type: json_invalid, msg: JSON decode error
```

## Optional fields

A field given a default value is optional:

```python
class Book(BaseModel):
    title: str
    year: int
    tags: list[str] = []
    note: str | None = None
```

When `{"title": "Dune", "year": 1965}` is sent, `tags` becomes `[]` and
`note` `null`. The same rule as for query parameters: no default means
required.

## Extra fields are dropped silently

`{"title": "Dune", "year": 1965, "extra": 1}` → `201`, but `extra` is not in
the model and is **dropped** (measured). This is also a safety feature: even
if a client sends `{"is_admin": true}`, it does not reach your code unless
your model has such a field. The drawback: a misspelt field (`"yaer"`)
disappears without an error; you get `422` for the missing `year` and find
the cause from there.

## Nested models

A model can contain another model as a field:

```python
class Author(BaseModel):
    name: str


class BookWithAuthor(BaseModel):
    title: str
    author: Author
```

When `{"title": "Emma", "author": {"name": "Austen"}}` is sent,
`item.author` is an `Author` object and `item.author.name` is `"Austen"`.
Lists work too: `items: list[Item]`.

## Returning a model

A function can return the model directly; FastAPI turns it into JSON:

```python
@app.post("/echo")
def echo(book: Book):
    return book
```

```text
POST /echo  {"title": "Dune", "year": 1965, "tags": ["sf"]}
200         {"title":"Dune","year":1965,"tags":["sf"],"note":null}
```

## Path + body together

When updating a record, which record comes from the path and the new values
from the body:

```python
@app.put("/books/{book_id}")
def replace_book(book_id: int, book: Book):
    ...
```

FastAPI tells the three sources apart by the parameter's shape:

| Parameter | From where? |
|---|---|
| The address has `{book_id}` | Path |
| A simple type (`int`, `str`...), not in the address | Query |
| A Pydantic model | Body |

## In `/docs`

When `POST /books` is opened, Swagger UI shows a ready example for the body
(`{"title": "string", "year": 0, ...}`) and lists the `Book` schema below:
the fields, the types, which are required. All of this came from the model.

## Summary

- The body's template is a Pydantic model: `class Book(BaseModel)` + typed
  fields.
- A parameter typed with a model is read from the body; `book.title`,
  `book.model_dump()`.
- A body that does not fit gives `422` (`loc: ["body", ...]`); conversions
  that lose nothing (`"1965"` → `1965`) are made.
- A field with a default is optional; extra fields are dropped.
- Path + query + body can be used together in the same endpoint.
