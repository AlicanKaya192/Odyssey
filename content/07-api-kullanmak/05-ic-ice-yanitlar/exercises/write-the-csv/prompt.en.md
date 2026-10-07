The last step: write the rows you flattened to a file. Both Excel and pandas
can open a CSV file.

**What to do:**

1. From every book, build a row with the columns `id`, `title`, `price` (a
   **float**), `author_name` and `tags` (joined with `|`).
2. Write the rows to `books.csv` with `csv.DictWriter`: first the header line
   (`writeheader`), then the rows (`writerows`). Open the file with
   `newline=""` and `encoding="utf-8"`.
3. Open the file again and print its contents as they are.

**Expected output:**

```
id,title,price,author_name,tags
1,Emma,12.5,Austen,classic|novel
2,Dune,9.99,Herbert,scifi|classic
3,Ulysses,15.0,Joyce,
4,Solaris,11.2,Lem,scifi
5,Persuasion,8.75,Austen,classic|romance|novel
```

Ulysses has no tags, so its last column is empty: the line ends with a
comma.
