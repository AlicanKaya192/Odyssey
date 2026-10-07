Write the raw response to disk; on the second call do not go to the API at
all.

**What to do:**

1. Write the function `load_books(session)`: if the file `books_raw.json`
   exists, it reads and returns it and prints `from cache`; otherwise it
   fetches with `fetch_all`, writes the file, prints `from api` and returns
   the books.
2. Call `load_books` **twice**; print the number of books each time.

`get_json` and `fetch_all` are given.

**Expected output:**

```
from api
books: 23
from cache
books: 23
```

The check makes sure only 2 requests in total were sent across the two
calls.
