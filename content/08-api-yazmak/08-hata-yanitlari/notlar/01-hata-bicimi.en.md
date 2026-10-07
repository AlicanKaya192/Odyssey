All of an API's error answers should look **the same**. Whoever writes the
client should be able to read the error from the same place at every
endpoint.

## A good error body

```json
{"detail": {"code": "out_of_stock", "message": "Book is out of stock", "item": "book"}}
```

| Field | Who reads it? | What for? |
|---|---|---|
| `code` | Programs | Fixed, short, English: `out_of_stock`, `name_taken` |
| `message` | People | An explanation; it may change |
| Extra fields | Both | Which record, which field: `item`, `field` |

The message's wording will change one day; `code` never does. The client's
code should decide by looking at `code`.

## Things to avoid

- **Different codes for the same situation:** `404` in one place, `400`
  "not found" in another.
- **`200` for an error:** `200 {"error": "not found"}` misleads the client;
  most clients look at the status code first.
- **Leaking the insides:** `detail=str(exc)` may send out a database query,
  a file path or user data.
- **Deciding by text meant for people** (on the client side): the code
  breaks the day the message changes.

## `HTTPException` or your own exception?

| Situation | Choice |
|---|---|
| A simple `404` inside the endpoint | `HTTPException` |
| The error is in a helper, in business logic | Your own exception class + a handler |
| The same error in many endpoints | Your own exception class + a handler |

Your own exception class separates the business logic from HTTP: the
`take()` function could be used in a command-line tool tomorrow.

## The handler's signature

```python
@app.exception_handler(OutOfStock)
def handler(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=..., content={...})
```

Two parameters (the request and the exception) and a `JSONResponse`. You
reach the exception object's fields (`exc.item`) from here.
