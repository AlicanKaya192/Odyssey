The first line of every HTTP request has three parts: the method, the
target and the version, separated by single spaces.

**What to do:**

1. Write the function `parse_request_line(line)`. It returns this
   dictionary: `{"method": ..., "target": ..., "version": ...}`.
2. For every line in the `lines` list, print the method and the target in
   the format below.

**Expected output:**

```
GET -> /v1/books?author=Austen
POST -> /v1/books
DELETE -> /v1/books/42
```
