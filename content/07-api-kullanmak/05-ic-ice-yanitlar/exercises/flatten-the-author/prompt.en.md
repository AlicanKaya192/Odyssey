You will build one table row from every book. `author` is a nested
dictionary, Herbert's record has no `country`, and the price arrived as text.

**What to do:**

1. Build a list called `rows`. Each row is a dictionary with these keys:
   `id`, `title`, `price` (a **float**), `author_name`, `author_country`
   (`"unknown"` if missing).
2. Print each row with its values separated by `|`.
3. On the last line, print the sum of the prices with two decimals.

**Expected output:**

```
1 | Emma | 12.5 | Austen | UK
2 | Dune | 9.99 | Herbert | unknown
3 | Ulysses | 15.0 | Joyce | IE
4 | Solaris | 11.2 | Lem | PL
5 | Persuasion | 8.75 | Austen | UK
total price: 57.44
```
