`headers` is a dictionary of lower-case header names, `allowed` the
allowed origins (`"https://bank.example"`). `origin_ok(headers, allowed)`:
if there is an `origin` header, is it in the allow list; otherwise, if
there is a `referer`, is its origin (`scheme + "://" + netloc`, with
`urlsplit`) in the list; if neither, `False`.

**Expected output:**

```
True
False
True
False
```
