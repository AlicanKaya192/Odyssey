You need the 7 newest books. Fetching every page is unnecessary: stop once
you have collected enough.

**What to do:**

1. Write the function `newest(n)`: it asks page by page with `sort=-year`
   and `per_page=5`, stops when it reaches `n` books (or the pages run out)
   and returns **the titles of the first `n` books**.
2. Call `newest(7)` and print the titles.

**Expected output:**

```
Fiasco
The Dispossessed
The Lathe of Heaven
Dune Messiah
The Left Hand of Darkness
A Wizard of Earthsea
Dune
```

The check makes sure the main program sends at most 2 requests.
