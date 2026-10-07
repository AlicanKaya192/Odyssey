`/cursor/books` pages with a cursor: the response is `{"results": [...],
"next_cursor": ...}`. The first request has no cursor; on the following ones
you send the previous response's `next_cursor` back with the `cursor`
parameter.

**What to do:**

1. Write the function `fetch_all()`: it collects all books with the cursor
   and returns **the list of titles**. It stops when `next_cursor` is
   `None`.
2. Call the function; print how many books came, and the first and last
   title.

**Expected output:**

```
books: 23
first: Emma
last: The Lathe of Heaven
```

Do not interpret the cursor; send it back as it is.
