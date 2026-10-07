# Validation

In the previous section Pydantic checked the body's **types**: is `year` an
integer, is `title` a string. But even with the right type a value can be
nonsense: `year` `-500`, `title` an empty string, a page size of `10000`.
In this section you put rules on the **value itself**; a request that
breaks them never reaches your function.

## Why does the server check?

The client (a browser, a mobile app) can check too, but you can't trust
it: anyone can send whatever body they like with `requests` or `curl`.
The server is the one that stores and uses the data, so **the server has
the last word**. In FastAPI you don't do this with piles of `if`s but with
rules written next to the field.

## `Field`: a field's rules

```python
from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1450, le=2100)
    rating: float = Field(default=0, ge=0, le=5)
    isbn: str | None = Field(default=None, pattern=r"^[0-9]{13}$")
```

- For numbers: `gt` (greater than), `ge` (greater or equal), `lt` (less
  than), `le` (less or equal).
- For strings: `min_length`, `max_length` and `pattern` (a regular
  expression).
- With `default=` the field becomes optional, just like writing `= 0`.

`pattern=r"^[0-9]{13}$"`: exactly 13 digits from the start (`^`) to the end
(`$`). You don't need to know regular expressions in detail; the most
common ones are in the note.

<figure class="fig">
  <div class="flow">
    <span class="node">Body<br><small>JSON</small></span><span class="arrow">→</span>
    <span class="node">Type<br><small>year: int</small></span><span class="arrow">→</span>
    <span class="node acc">Rule<br><small>Field(ge=1450)</small></span><span class="arrow">→</span>
    <span class="node acc">Validator<br><small>field_validator</small></span><span class="arrow">→</span>
    <span class="node ok">Your function</span>
  </div>
  <figcaption>The request passes three checks in turn. If it fails any of them your function is never called and <code>422</code> goes back.</figcaption>
</figure>

## What we measured

| Sent | Result |
|---|---|
| `{"title": "Dune", "year": 1965}` | `200`, `rating` `0.0`, `isbn` `null` |
| `{"title": "", "year": 1965}` | `422` string_too_short |
| `{"title": "Dune", "year": 3000}` | `422` less_than_equal |
| `{"title": "Dune", "year": 1965, "rating": 7}` | `422` less_than_equal |
| `{"title": "Dune", "year": 1965, "isbn": "123"}` | `422` string_pattern_mismatch |

The error body states the rule too:

```json
{"type": "less_than_equal", "loc": ["body", "year"],
 "msg": "Input should be less than or equal to 2100",
 "input": 3000, "ctx": {"le": 2100}}
```

If several fields are broken, **all** of them come in one answer:
`{"title": "", "year": 3000}` returned a `detail` list with two errors. The
client can fix every error at once.

## Rules in the path and query

Query and path parameters take the same rules. For that, `Query` or `Path`
is written next to the type, both inside `Annotated`:

```python
from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/books")
def list_books(limit: Annotated[int, Query(ge=1, le=50)] = 10):
    return {"limit": limit}


@app.get("/books/{book_id}")
def get_book(book_id: Annotated[int, Path(gt=0)]):
    return {"id": book_id}
```

`Annotated[int, Query(ge=1, le=50)]` means "the type is `int`, the extra
information is `Query(...)`". The default still goes at the end with `= 10`.

```text
GET /books?limit=100   422  less_than_equal, loc ["query", "limit"]
GET /books?limit=0     422  greater_than_equal
GET /books             200  {"limit": 10}
GET /books/0           422  greater_than, loc ["path", "book_id"]
```

The first item of `loc` says where the error is: `body`, `query` or `path`.

## Only certain values: `Literal`

If a field may take only one of a few values:

```python
from typing import Literal


class Order(BaseModel):
    size: Literal["small", "medium", "large"]
```

`{"size": "huge"}` → `422` literal_error, and the message lists the
options: `Input should be 'small', 'medium' or 'large'`. The `/docs` page
shows this field as a drop-down too.

## Your own rule: `field_validator`

When the ready-made rules aren't enough, you write your own check:

```python
from pydantic import BaseModel, field_validator


class User(BaseModel):
    name: str
    username: str

    @field_validator("username")
    @classmethod
    def no_spaces(cls, value: str) -> str:
        if " " in value:
            raise ValueError("must not contain spaces")
        return value.lower()
```

- The function receives the field's value (**after** the type check, so
  `value` is certainly a string here).
- If the rule is broken you raise `ValueError`; Pydantic turns it into a
  `422`.
- What you return becomes the field's new value: here it was lower-cased.

```text
{"username": "ada lovelace"}  422  value_error, "Value error, must not contain spaces"
{"username": "AdaL"}          200  {"name": "Ada", "username": "adal"}
```

The `@classmethod` line is the pattern from Pydantic's docs. It works even
without it (we measured), but it tells the reader that the first parameter
is the class, not an object; write it.

## Checking two fields together: `model_validator`

A rule like "the end can't be before the start" doesn't belong to one
field. A check that runs after the whole model is filled:

```python
from pydantic import BaseModel, model_validator


class Trip(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_order(self):
        if self.end < self.start:
            raise ValueError("end must not be before start")
        return self
```

`mode="after"`: after the fields are checked; the function takes `self` and
**must return `self`**. The error's `loc` is not a field but the body
itself: `["body"]`.

## The whitespace trap

We sent `"  "` (two spaces) to a name with `Field(min_length=1)`: **`200`**.
Two spaces are two characters. To strip the edges first, add to the model:

```python
from pydantic import BaseModel, ConfigDict, Field


class Author(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1)
```

Now `"  "` → `422`, and `"  Ada "` → `"Ada"`.

## Summary

- A value's rules sit next to the field: `Field(ge=..., le=..., min_length=...,
  max_length=..., pattern=...)`.
- In the query and path: `Annotated[int, Query(...)]`, `Annotated[int, Path(...)]`.
- One of a set of options: `Literal[...]`.
- Your own rule: `@field_validator` (one field), `@model_validator(mode="after")`
  (fields together); the error is `ValueError`, the result `422`.
- All errors come in one answer; `loc` says where, `type` says what.
