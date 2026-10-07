You have the raw text of a response that came back with `429`. You will do
what a request library does when it reads a response.

**What to do:**

1. Write the function `parse_response(raw)`. It splits the text in two at the
   first blank line (`"\n\n"`); it takes the code (int) from the first line
   and the headers (names lower-cased) from the lines after it. It returns
   `{"code": ..., "headers": {...}, "body": ...}`.
2. Read the response with `response = parse_response(raw)` and print:
   - the code,
   - the part of the content type **before the semicolon**,
   - the `Retry-After` value as a **number**, as `wait 30 seconds`,
   - the body.

**Expected output:**

```
429
application/json
wait 30 seconds
{"error": "rate limit", "limit": 60}
```
