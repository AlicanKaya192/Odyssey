The first digit of a status code gives its class. Turn that into a function.

**What to do:**

1. Write the function `status_class(code)`. Based on the first digit
   (`code // 100`) it returns one of: `"info"` (1), `"success"` (2),
   `"redirect"` (3), `"client error"` (4), `"server error"` (5).
2. For every code in the `codes` list, print the code and its class.

**Expected output:**

```
200 success
201 success
304 redirect
404 client error
429 client error
500 server error
503 server error
```
