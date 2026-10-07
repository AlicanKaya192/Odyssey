# Path Parameters

In a books API every book has its own address: `/books/1`, `/books/2`,
`/books/42`. Writing a separate function for each book is impossible.
Instead you define the changing part of the address as a **path
parameter**: one function, endless addresses.

## Reserving a place with curly braces

```python
books = {1: {"id": 1, "title": "Dune"}, 2: {"id": 2, "title": "Emma"}}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return books[book_id]
```

- `{book_id}` sets that part of the address aside as a **variable**.
- The function's parameter is written with **the same name** (`book_id`);
  FastAPI puts the value from the address there.
- `: int` tells FastAPI "this must be an integer".

<figure class="fig">
  <div class="anat">
    <div class="sig"><code>GET /books/<b>2</b></code> → <code>@app.get("/books/<b>{book_id}</b>")</code> → <code>get_book(<b>book_id</b>: int)</code></div>
    <div class="legend">
      <div><b>2</b> the text from the address: <code>"2"</code></div>
      <div><b>{book_id}</b> this part of the address is a variable</div>
      <div><b>book_id: int</b> the same name; FastAPI converts <code>"2"</code> to <code>2</code></div>
    </div>
  </div>
  <figcaption>The part of the address, the name in curly braces and the function's parameter are linked by the same name.</figcaption>
</figure>

## Type: converting and checking

An address is always text: when `/books/2` comes, you have `"2"`. Because
you wrote `book_id: int`, FastAPI **converts it to a number**; inside the
function `book_id` is `2` (an integer) and you can look it up in the
dictionary as `books[2]`.

If it cannot be converted, the request is rejected without the function
ever being called (measured):

```text
GET /books/2      200  {"book_id": 2, "type": "int"}
GET /books/abc    422
GET /books/2.5    422
```

The body of the `422` says what is wrong:

```json
{"detail": [{
  "type": "int_parsing",
  "loc": ["path", "book_id"],
  "msg": "Input should be a valid integer, unable to parse string as an integer",
  "input": "abc"}]}
```

| Field | Meaning |
|---|---|
| `loc` | Where: `book_id` in the `path` |
| `msg` | What was expected |
| `input` | What came |

This is exactly the body you read when you got a `422` from an API in
API 1. This time you did not write it; FastAPI produced it from the type
hint.

Without a type (`def get_book(book_id):`) the value stays text and
`books["2"]` is not found; always write the type.

## A record that is not found: 404

`/books/99` is a valid number but there is no such book. `books[99]` raises
a `KeyError` and the client gets `500`: it looks like a server error,
whereas the mistake is in the record the client asked for. The right answer
is `404`:

```python
from fastapi import FastAPI, HTTPException


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
```

`raise HTTPException(...)` stops the function right there and answers the
client with the given code and the body `{"detail": "Book not found"}`. We
will see the details in the Error Responses section; for now knowing the
pattern is enough.

## Text parameters and spaces

```python
@app.get("/hello/{name}")
def hello(name: str):
    return {"greeting": "Hello, " + name}
```

`GET /hello/Ada` → `{"greeting": "Hello, Ada"}`. A space comes in the
address as `%20` (`/hello/Ada%20Lovelace`); FastAPI decodes it into
`"Ada Lovelace"`.

## Several parameters

```python
@app.get("/users/{user_id}/books/{book_id}")
def user_book(user_id: int, book_id: int):
    return {"user": user_id, "book": book_id}
```

`GET /users/7/books/3` → `{"user": 7, "book": 3}`. One parameter with the
same name for every pair of curly braces.

## The ordering trap

Think of two endpoints: `/books/{book_id}`, which gets a book by its id, and
`/books/latest`, which gets the newest book. If you write them in this
order:

```python
@app.get("/books/{book_id}")
def get_book(book_id: int): ...


@app.get("/books/latest")
def latest(): ...
```

`GET /books/latest` goes to the **first** matching path: `{book_id}` catches
everything, `"latest"` cannot be converted to a number and `422` comes back
(measured). `latest` is never called.

The rule: **write fixed paths before paths with variables.**

```python
@app.get("/books/latest")
def latest(): ...


@app.get("/books/{book_id}")
def get_book(book_id: int): ...
```

## In the docs

On the `/docs` page `book_id` appears as a "path" parameter of type
`integer`, required; "Try it out" opens a box and asks for the value. This,
too, came from the type hint.

## Summary

- `"/books/{book_id}"` + `def f(book_id: int)`: the name must be the same in
  both.
- The type hint converts and checks the value; if it does not fit, `422` and
  a body that says where the error is.
- For a missing record, `raise HTTPException(status_code=404, detail=...)`;
  otherwise `500`.
- Fixed paths (`/books/latest`) before paths with variables
  (`/books/{book_id}`).
