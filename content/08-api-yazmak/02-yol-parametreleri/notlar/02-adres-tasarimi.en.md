The address rules you saw while reading REST in the Using APIs module, this time as the one
who writes the address.

## Resource and id

| Address | Meaning |
|---|---|
| `/books` | All the books (the collection) |
| `/books/42` | The book whose id is 42 |
| `/authors/7/books` | The books of author 7 |
| `/authors/7/books/3` | Book 3 of that author |

- Plural nouns, lowercase, hyphens between words: `/book-reviews`.
- At most two levels of nesting; deeper becomes unreadable. If needed, a
  query parameter: `/books?author_id=7` (Query Parameters section).
- The id is usually a number (`/books/42`); a readable name (`/books/dune`)
  is possible too, but when the name changes, the address changes.

## Nouns, not verbs

| Instead of | Write |
|---|---|
| `GET /getBook/42` | `GET /books/42` |
| `POST /books/42/delete` | `DELETE /books/42` |
| `GET /books/create?title=Dune` | `POST /books` (with a body) |

## Order

Endpoints are tried **in the order they are written**, the first match
wins. Paths with fixed parts first:

```python
@app.get("/books/latest")       # 1. fixed
@app.get("/books/{book_id}")    # 2. with a variable
```

Two paths with variables in the same place are not written either:
`/books/{book_id}` and `/books/{title}` catch the same addresses; the
second never runs.

## Keep in mind

> An address is the name of a thing; the method says what to do. Every pair
> of curly braces in the address is a parameter with the same name and a
> type in the function.
