You are going to write your first class.

**What you need to do:**

1. Write a class called `Book`.
2. Its constructor (`__init__`) takes two things: `title` and `pages`. Make
   both of them attributes of the object.
3. Write a method called `is_long`: it returns `True` when the page count is
   **300 or more**, and `False` otherwise.
4. Build two books and print the results:
   - `long_book` — `"Ulysses"`, 730 pages
   - `short_book` — `"Notes"`, 120 pages

**Expected output:**

```
Ulysses
True
Notes
False
```

In order: the long book's title, its `is_long` result, the short book's title,
its `is_long` result.

> The first parameter of every method has to be `self`. You reach the object's
> data with `self.pages`.
