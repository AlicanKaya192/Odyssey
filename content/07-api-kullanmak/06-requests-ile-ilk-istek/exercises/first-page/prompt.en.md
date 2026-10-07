`GET /books` returns the list of books. The response is an envelope: the books
are in `data`, the page information in `meta` (Section 05).

**What to do:**

1. Send a request to `http://api.odyssey.test/books`.
2. Collect the titles of the books on this page into a list called
   `titles`.
3. Print the total number of books, the number on this page and the titles
   in the format below.

**Expected output:**

```
total: 23
on this page: 5
Emma
Dune
Ulysses
Solaris
Persuasion
```
