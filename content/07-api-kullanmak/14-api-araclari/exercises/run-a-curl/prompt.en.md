Run the curl command you copied from the documentation in Python.
`parse_curl` is given (the solution of the previous exercise).

**What to do:**

1. Take the command apart with `parse_curl(command)`.
2. Send the request with `requests.request(method, url, headers=...,
   data=...)`. The body is text, so use `data=`; the `Content-Type` header is
   already in the command.
3. Print the status code, the `Location` header and the `title` in the
   response.

**Expected output:**

```
status: 201
location: /books/24
title: Kindred
```
