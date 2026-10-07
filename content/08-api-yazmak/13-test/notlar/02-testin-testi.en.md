A passing test proves nothing on its own: a test that checks nothing also
passes. A good test **fails on broken code**.

## Ask yourself: if I broke this line, would a test fail?

```python
@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
```

| Breakage | Which test catches it? |
|---|---|
| The `raise` line is deleted | A test expecting `404` for a missing book |
| `400` written instead of `404` | The same test, if it checks the code |
| `return {}` instead of `return books[book_id]` | A test that checks the body |

A test that only writes `assert r.status_code == 200` doesn't catch the
third.

## What Odyssey does

In this section's exercises your tests are run first as they are, then
against **deliberately broken** versions of the application. For every
broken version at least one test must fail; if none does, the terminal
says which bug it missed (for example "a missing book returns 200 instead
of 404").

In the software world this is called **mutation testing**: changing the
code in small ways and seeing whether the tests notice.

## What not to test?

- FastAPI itself: no need to check every field of the `422` `detail` list
  one by one; the status code is enough.
- The random values themselves: a token's content differs every time; check
  its length or presence.
