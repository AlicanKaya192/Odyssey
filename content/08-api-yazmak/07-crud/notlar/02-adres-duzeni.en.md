In REST APIs addresses follow a certain pattern. It's convention, not a rule;
but if you follow it, people using your API can guess without reading the
docs.

## A noun, not a verb

The address says **what** is worked on, the method says **what is done**.

| Bad | Good |
|---|---|
| `POST /createBook` | `POST /books` |
| `GET /getBook?id=3` | `GET /books/3` |
| `POST /deleteBook/3` | `DELETE /books/3` |
| `POST /books/3/update` | `PATCH /books/3` |

## A plural noun

The collection is plural: `/books`, `/users`. One record sits under the
collection: `/books/3`. The same word in both.

## Nested resources

An author's books: `GET /authors/7/books`. Adding a new book to that author:
`POST /authors/7/books`. Don't go deeper than one level; instead of
`/authors/7/books/3/reviews/2`, use `/reviews/2`.

## Filtering, sorting, paging in the query

`GET /books?year=1965&sort=title&limit=20&offset=40`. Don't open a new
address (`/books/by-year/1965`).

## The answer's code

| Request | Answer |
|---|---|
| `POST /books` | `201`, the new record, `Location: /books/4` |
| `GET /books` | `200`, a list (`[]` if empty, not `404`) |
| `GET /books/4` | `200` or `404` |
| `PUT` / `PATCH /books/4` | `200`, the current record |
| `DELETE /books/4` | `204` |

An empty list isn't an error: "there are no books" is a valid answer too.
