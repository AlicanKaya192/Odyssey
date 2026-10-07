Add one of Le Guin's books to the library.

**What to do:**

1. Send the `new_book` dictionary with `POST /books`, using `json=` and
   `headers=AUTH`.
2. Print the status code, the `Location` header, the number the server
   assigned and the author's name from the response.

**Expected output:**

```
status: 201
location: /books/24
id: 24
author: Le Guin
```
