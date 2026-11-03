`parse_headers(text)` should turn headers given line by line (`\n`)
into a dictionary. The name and value are split at the **first** `:`; the
name is turned to lower case and the leading and trailing spaces of both
are removed. A line with no `:` is skipped.

**Expected output:**

```
host = shop.example.com
cookie = session=abc123
x-mode = test
```
