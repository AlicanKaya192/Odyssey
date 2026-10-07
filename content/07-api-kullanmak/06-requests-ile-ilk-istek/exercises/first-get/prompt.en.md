You are sending your first real request. Ask the practice server for book number 1.

**What to do:**

1. Send a request to `http://api.odyssey.test/books/1` with `requests.get`.
2. Print the status code, the `ok` value, the book's title and its author's
   name in the format below. The author is in the book's `author`
   dictionary.

**Expected output:**

```
status: 200
ok: True
title: Emma
author: Austen
```

When you run it, the terminal will also show your request:
`→ GET /books/1  200`.
