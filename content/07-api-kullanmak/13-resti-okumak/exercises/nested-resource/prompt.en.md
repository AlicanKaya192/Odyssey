Get Le Guin's books from the nested resource address. You do not know the
author's number; find it in the author list first.

**What to do:**

1. Get the authors with `GET /authors` and put the identifier of the one
   named `Le Guin` into the `author_id` variable.
2. Ask for their books with `GET /authors/<author_id>/books`.
3. Print the identifier, the number of books, and the titles with their
   years.

**Expected output:**

```
author id: 6
books: 4
1974 The Dispossessed
1969 The Left Hand of Darkness
1968 A Wizard of Earthsea
1971 The Lathe of Heaven
```
