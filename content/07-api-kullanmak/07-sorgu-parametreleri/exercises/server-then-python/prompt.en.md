You want classics cheaper than 10, but the server cannot filter by price
(there is no `price_max`). Narrow down as far as the server can and filter
the rest in Python.

**What to do:**

1. Send `tag=classic` and `per_page=20` in **a single request**.
2. From the books that come back, put the ones with a price below 10 into a
   `cheap` list (the dictionaries themselves).
3. Sort them by price and print the title and price; at the end print how
   many books there are.

**Expected output:**

```
Animal Farm 6.9
Dubliners 7.8
Persuasion 8.75
Sense and Sensibility 9.1
Mrs Dalloway 9.3
Nineteen Eighty-Four 9.5
To the Lighthouse 9.8
Dune 9.99
cheap classics: 8
```

The check also makes sure only **one** request was sent: do not send a
separate request for every book.
