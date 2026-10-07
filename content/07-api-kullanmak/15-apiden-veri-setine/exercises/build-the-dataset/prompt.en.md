The whole pipeline: fetch, flatten, check, write.

**What to do:**

1. Write the function `to_row(book)`: it returns a dictionary with the keys
   `id`, `title`, `author` (the author's name), `country`, `year` (int),
   `price` (float), `tags` (joined with `|`).
2. Fetch every book with `fetch_all` and turn them into rows.
3. Check: identifiers must be unique and there must be 23 rows (`assert`).
4. Write them to `books.csv` with `csv.DictWriter` (`newline=""`, `utf-8`).
5. Open the file again and print its first three lines and the total number
   of rows (excluding the header).

**Expected output:**

```
id,title,author,country,year,price,tags
1,Emma,Austen,UK,1815,12.5,classic|novel
2,Dune,Herbert,US,1965,9.99,scifi|classic
rows: 23
```
