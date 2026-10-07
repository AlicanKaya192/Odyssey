Practice reading real API addresses. For each one ask yourself: which
computer, which door, which extra details?

## Example 1

```text
https://api.github.com/repos/python/cpython/issues?state=open&per_page=5
```

- Host `api.github.com`: GitHub's API (the site is `github.com`).
- Path `/repos/python/cpython/issues`: the issues of the "cpython" repository
  of the "python" account. The pieces of the path narrow down towards one
  resource.
- Query: only open ones (`state=open`), 5 per page (`per_page=5`). We will
  see the idea of "pages" in Section 10.

## Example 2

```text
http://localhost:8000/books/42
```

- `http`, `localhost`, `8000`: a server you are trying out on your own
  computer.
- Path `/books/42`: book number 42. No query string.

## Example 3

```text
https://api.example.com/v2/search?q=fish+%26+chips&lang=en
```

- `v2`: the second version of the API.
- The value of `q` is encoded: `+` is a space and `%26` is `&`. Decoded, it
  reads `fish & chips`.

## Path or query?

The same information can go in either place: `/books/42` or `/books?id=42`.
The general rule:

- If it points to **a single resource**, use the **path**: `/books/42`.
- If it **filters, sorts or pages a list**, use the **query**:
  `/books?author=Austen&sort=year`.

The API's author decides which one is used; you check the documentation.

## Spot the mistake

Each of these addresses has a problem:

1. `https://api.example.com/v1weather` → the `/` between the base and the
   endpoint is missing.
2. `https://api.example.com/search?q=new york` → the space is not encoded.
3. `https://api.example.com/search?q=a?lang=en` → the second `?` should be
   an `&`.
4. `https://api.example.com/books#42` → everything after `#` stays in the
   browser; the book number never reaches the server.
