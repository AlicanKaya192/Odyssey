You will try to add four books; three of them break the rules. You will read
and print what the server says.

**What to do:** for every book in the `books` list:

1. Send it with `POST /books` (`json=`, `headers=AUTH`).
2. If the code is `201`, print `created` and the `Location`; otherwise print
   the status code and the `detail` from the body.

**Expected output:**

```
422 title must be a non-empty string
422 price must be a positive number
422 author_id does not exist
created /books/24
```
