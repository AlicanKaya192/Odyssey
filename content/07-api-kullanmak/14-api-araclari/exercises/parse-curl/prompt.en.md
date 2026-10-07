Documentation examples are curl commands. You will write a function that
takes a command apart and extracts the request's details.

**What to do:** write the function `parse_curl(command)`. Split the command
with `shlex.split` and read the pieces after `curl` in order:

- `-X` → the next piece is the method,
- `-H` → the next piece is a header (`"Name: value"`, split at the first
  `": "`),
- `-d` → the next piece is the body,
- any other piece → the address.

If no method is given: `"POST"` when there is a body, otherwise `"GET"`.
Return `{"method": ..., "url": ..., "headers": {...}, "data": ... or None}`.

Then for every command in the `commands` list, print the method, the
address, the number of headers and the body.

**Expected output:**

```
GET http://api.odyssey.test/books/1 0 None
GET http://api.odyssey.test/stats 1 None
POST http://api.odyssey.test/books 2 {"title": "Kindred", "price": 11.5}
```
