You will do a request library's job with a small function: build the text of
the request.

**What to do:** write the function `build_request(method, target, host,
body="")`. The text it returns is made of lines joined with `"\n"`:

1. The request line: `<method> <target> HTTP/1.1`
2. `Host: <host>`
3. If `body` is not empty, two more headers:
   `Content-Type: application/json` and `Content-Length: <byte count>`.
   The byte count is `len(body.encode("utf-8"))`.
4. After the headers, a blank line, then `body`.

In other words, the text is the header lines joined with `"\n"` +
`"\n\n"` + `body`.

Then print the two requests below with `---` between them.

**Expected output:**

```
GET /v1/books?author=Austen HTTP/1.1
Host: api.example.com


---
POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 17

{"title": "Emma"}
```

The `GET` request has no body; its text ends with the blank line.
