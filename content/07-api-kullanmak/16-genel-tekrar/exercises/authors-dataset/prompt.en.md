A review of Sections 05, 13 and 15: build a dataset from nested resources.

**What to do:**

1. Get the authors with `GET /authors`.
2. For each author ask for their books with `GET /authors/<id>/books`; build
   a row with the number of books, the earliest and latest year and the
   average price (two decimals): `name`, `country`, `books`, `first`,
   `last`, `avg_price`.
3. Write the rows to `authors.csv`.
4. Read the file and print its contents.

**Expected output:**

```
name,country,books,first,last,avg_price
Austen,UK,4,1811,1817,10.19
Herbert,US,2,1965,1969,10.45
Joyce,IE,2,1914,1922,11.4
Lem,PL,3,1961,1986,12.2
Orwell,UK,3,1938,1949,8.83
Le Guin,US,4,1968,1974,10.09
Tolstoy,RU,2,1869,1878,16.1
Woolf,UK,3,1925,1928,9.23
```
