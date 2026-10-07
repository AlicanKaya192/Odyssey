A server learns where the body ends from `Content-Length` when it reads a
request. If the header is wrong, the body is cut short or the server waits
for bytes that never come. You will write a small piece that checks an
incoming request.

**What to do:** write the function `check_length(raw)`:

1. Split the text in two at the **first** blank line (`"\n\n"`): the top
   part is the request line + headers, the bottom part is the body.
   (`raw.split("\n\n", 1)` or `raw.partition("\n\n")`.)
2. Find the `Content-Length` value among the headers (search with the name
   lower-cased) and turn it into a number.
3. Work out the real byte count of the body.
4. If the two are equal return `"ok"`, otherwise return
   `"mismatch: declared 50, actual 38"`.

Then check the two requests and print the results.

**Expected output:**

```
good: ok
bad: mismatch: declared 50, actual 38
```
