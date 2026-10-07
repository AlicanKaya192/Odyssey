The base address sometimes ends with `/` and sometimes does not; the
endpoint sometimes starts with `/` and sometimes does not. In all four cases
the result must be joined with **exactly one** `/`.

**What to do:**

1. Write the function `endpoint_url(base, path)`: it cleans the slashes on
   the right of the base and on the left of the path and puts a single `/`
   in between.
2. Print the four joins below.

**Expected output:**

```
https://api.example.com/v1/weather
https://api.example.com/v1/weather
https://api.example.com/v1/weather
https://api.example.com/v1/books/42
```
