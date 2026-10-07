Some book numbers do not exist on the server. Code that reads the body without
checking the status code fails on them.

**What to do:**

1. Write the function `get_title(book_id)`: it sends a request to
   `/books/<book_id>`; if the status code is `200` it returns the book's
   title, otherwise `None`.
2. For every number in the `ids` list, print the number and the result.

**Expected output:**

```
4 -> Solaris
99 -> None
12 -> Animal Farm
0 -> None
```
