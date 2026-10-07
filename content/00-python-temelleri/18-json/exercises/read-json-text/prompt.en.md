The variable `text` holds the JSON text of a book.

**What to do:**

1. Import the `json` module.
2. Turn the text into a dictionary called `book` with `json.loads`.
3. Print, in order: the type of `book` (`type(book)`), the book's title and
   author (with `by` between them), how old the book is in 2026
   (`2026 - book["year"]`) and `book["available"]`.

**Expected output:**

```text
<class 'dict'>
Dune by Frank Herbert
61
True
```

`available` is written as `true` in the JSON; notice what it comes in as in
Python.
