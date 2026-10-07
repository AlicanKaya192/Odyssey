Combine filtering, sorting and limiting in one request: the three cheapest
books tagged `classic`.

**What to do:**

1. Send a request to `/books` with three parameters: `tag`, `sort`,
   `per_page`. (Smallest first: `sort=price`.)
2. Print the title and price of the books that come back.
3. On the last line print `meta.total`: the total number of classics.

**Expected output:**

```
Animal Farm 6.9
Dubliners 7.8
Persuasion 8.75
classics in total: 12
```
