The four patterns dependencies are used in, and where they help.

| Pattern | How | When? |
|---|---|---|
| Gives a value | `x: Annotated[T, Depends(f)]` | Shared parameters, finding a record |
| Only checks | `@app.get(..., dependencies=[Depends(f)])` | A key, a permission, a rate limit |
| Open/close | `def f(): ... yield ... finally:` | A database connection, a file |
| A chain | `def f(x: Annotated[T, Depends(g)])` | First the user, then their permission |

## Where does a dependency read from?

A dependency's parameters are filled by the same rules as an endpoint's:

| Parameter | Source |
|---|---|
| `{book_id}` in the address | Path |
| A simple type, not in the address | Query |
| `Annotated[str, Header()]` | A header (`x_key` → `X-Key`) |
| A Pydantic model | Body |
| `Annotated[T, Depends(g)]` | Another dependency |

## A named type

Give frequently used dependencies a name:

```python
Paging = Annotated[dict, Depends(paging)]
CurrentBook = Annotated[dict, Depends(get_book)]


@app.get("/books/{book_id}")
def read_book(book: CurrentBook):
    return book
```

Endpoints stay short, and "what does this endpoint need" can be read from
the first line.

## Common mistakes

The first three were measured:

| Mistake | Result |
|---|---|
| `Depends(paging())` (with parentheses) | `TypeError: {'limit': 10} is not a callable object` when the program starts |
| `print` instead of `return` in the dependency | `200`, the parameter is `null` |
| No `try/finally` in a `yield` dependency | If the endpoint fails, the closing **never runs** |
| Trying to use the result of a function given with `dependencies=` | The result doesn't reach the endpoint |

`Depends(paging)` takes **the function itself**, not a call to it.
