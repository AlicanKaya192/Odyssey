Animal Farm (number 12) has been discounted. Change only the price and verify
the result.

**What to do:**

1. First read the book with `GET` and print the old price.
2. Send only `{"price": 5.5}` with `PATCH /books/12`; print the status code.
3. Read the book again with `GET`; print the new price, and the year to show
   that it did not change.

**Expected output:**

```
old price: 6.9
patch: 200
new price: 5.5
year: 1945
```
