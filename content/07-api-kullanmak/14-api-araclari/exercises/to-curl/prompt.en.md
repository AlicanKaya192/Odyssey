Do the reverse: produce a curl command from a request's details. Very handy
when explaining a problem to someone or putting an example in documentation.

**What to do:** write the function `to_curl(method, url, headers)`. The
command is these pieces joined with spaces:

1. `curl`
2. If the method is not `GET`, `-X` and the method.
3. The address.
4. For each header `-H "Name: value"` (in double quotes, in the dictionary's
   order).

Then print the command for every request in the `samples` list.

**Expected output:**

```
curl https://api.example.com/books
curl https://api.example.com/stats -H "X-API-Key: abc"
curl -X DELETE https://api.example.com/books/7 -H "Authorization: Bearer abc"
```
