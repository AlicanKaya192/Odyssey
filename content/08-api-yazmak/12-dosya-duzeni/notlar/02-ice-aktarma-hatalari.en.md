The errors that come up when you split into files, and what they mean.

## A circular import

If `main.py` imports `models` and `models.py` imports `main`:

```text
ImportError: cannot import name 'Book' from 'models'
(consider renaming '...models.py' if it has the same name as a library ...)
```

That's Python 3.14's message (we measured). The "rename it" suggestion at
the end is **misleading** here: the real cause is that `main` asks for
`models` while it's still half-loaded (before `Book` is defined). The fix is
to make imports go one way: `models.py` imports no project files.

## `ModuleNotFoundError: No module named 'routers'`

- There's no `routers/__init__.py`, or
- the program is run from outside the project folder.

## `ImportError: cannot import name 'router' from 'routers.books'`

The variable in `routers/books.py` isn't called `router` (for example
`books_router`). The name in `main.py` and the name in the file must match.

## An endpoint doesn't show up (`404`)

- The `app.include_router(...)` line was forgotten.
- The prefix was written twice: with `prefix="/books"` on the router and the
  endpoint as `@router.get("/books")` → the address is `/books/books`.

## The same name in two files

If `routers/books.py` and `models.py` both define `Book`, which one is used
depends on the imports. Models live **only** in `models.py`.
