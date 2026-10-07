Apply the same change to two books with two different methods and see the
difference with your own eyes.

**What to do:**

1. Write the function `change_and_read(method, book_id)`: with
   `requests.request` it sends the body `{"title": "Changed", "price": 9.0}`
   to `/books/<book_id>` using the given method (`"PUT"` or `"PATCH"`), then
   reads the book with `GET` and returns it **as a dictionary**.
2. Apply `PATCH` to book 15 and `PUT` to book 14. For each, print the
   method, title, price, year and tags.

`requests.request("PATCH", url, ...)` is the general function that takes the
method as text; it does the same job as `requests.patch(url, ...)`.

**Expected output:**

```
PATCH Changed 9.0 1968 ['fantasy']
PUT Changed 9.0 0 []
```
