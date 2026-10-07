You will send requests to four addresses; two exist, two do not. Instead of
writing an `if` after every request, use `raise_for_status()`.

**What to do:** for every address in the `paths` list:

1. Send the request and call `raise_for_status()` right away.
2. If there is no error, print `ok`, the address and the `title` or `name`
   from the body (a book has `title`, an author has `name`; try both with
   `get`).
3. If a `requests.HTTPError` comes, print `failed`, the address and the
   status code.

**Expected output:**

```
ok /books/5 Persuasion
failed /books/0 404
ok /authors/3 Joyce
failed /authors/42 404
```
