The first step of the pipeline: get every book with a sturdy fetch function.
`get_json` is given (timeout, waiting on 429, retries).

**What to do:**

1. Write the function `fetch_all(session)`: it fetches `/books` with
   `get_json` in pages of `per_page=20` and returns every book once it
   reaches `meta.pages`.
2. Set up a `requests.Session`, call `fetch_all`; print the number of books
   and the titles of the first and last book.

**Expected output:**

```
books: 23
first: Emma
last: The Lathe of Heaven
```

The check makes sure only 2 requests were sent.
