The dataset is ready; now answer a question: how many books are there from the
authors of each country, and what is their average price?

**What to do:**

1. Fetch every book with `fetch_all`.
2. Gather the number of books and the price total per author country in a
   `by_country` dictionary (such as `{country: [count, total]}`).
3. Sort the countries by number of books, most first (by country name on a
   tie); for each print the country, the count and the average price (two
   decimals).

**Expected output:**

```
UK 10 books, average 9.49
US 6 books, average 10.21
PL 3 books, average 12.20
IE 2 books, average 11.40
RU 2 books, average 16.10
```
