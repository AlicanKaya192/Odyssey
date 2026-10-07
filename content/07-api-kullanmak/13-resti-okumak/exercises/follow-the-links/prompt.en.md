Move around using the links the root address gives, without memorising
addresses.

**What to do:**

1. Read the root address with `GET /`; print the `links` dictionary.
2. Follow the `links["books"]` link and print the total number of books
   (`meta.total`).
3. Follow the `links["authors"]` link and print the number of authors.

Do not write the addresses in your code (like `"/books"`); take them from the
links.

**Expected output:**

```
{'books': '/books', 'authors': '/authors', 'stats': '/stats'}
books: 23
authors: 8
```
