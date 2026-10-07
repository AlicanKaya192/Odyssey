`books.json` is the `/books` response of a book API. The records are under
the `data` key, the page information inside `meta`.

**What to do:**

1. Put the list of records into the variable `items`.
2. Collect the records' identifiers into a list called `ids`.
3. Print how many records you hold, the total number of records
   (`meta.total`), the identifiers, and how many pages are needed to get all
   of the data.

The number of pages: divide the total by the page size (`per_page`) and
**round up**. With integer arithmetic: `(total + per_page - 1) // per_page`.

**Expected output:**

```
on this page: 5
total: 23
ids: [1, 2, 3, 4, 5]
pages needed: 5
```
