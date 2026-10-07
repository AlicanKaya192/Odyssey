# Error Responses

A good API speaks clearly not only when things go well but also when they
**don't**. The client's code will read the error answer and decide:
retry, what to tell the user, which field to highlight. In this section you
design the error answers.

## FastAPI's own errors

Even without writing anything, FastAPI gives some errors by itself (we
measured):

```text
GET /nothing          404 {"detail": "Not Found"}            no such address
DELETE /items/pen     405 {"detail": "Method Not Allowed"}   no such method
GET /n?x=abc          422 {"detail": [{"type": "int_parsing", ...}]}
GET /boom             500 Internal Server Error             a bug in your code
```

In all of them the body comes with a `detail` key, except `500`: that's
plain text.

## `HTTPException`

To send your own error:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()
stock = {"pen": 3, "book": 0}


@app.get("/items/{name}")
def read_item(name: str):
    if name not in stock:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": name, "stock": stock[name]}
```

- `raise`, not `return`. The function stops on that line.
- `detail` becomes `{"detail": ...}` in the answer.

`detail` doesn't have to be a string; a dictionary works too and is more
useful for the client:

```python
raise HTTPException(status_code=409, detail={"code": "out_of_stock", "item": name})
```

```text
409 {"detail": {"code": "out_of_stock", "item": "pen"}}
```

A text message is read by people; a fixed field like `"code"` is read by
**programs**. The client can write
`if body["detail"]["code"] == "out_of_stock":`; even if the message's wording
changes, its code doesn't break.

A header can be added too:

```python
raise HTTPException(status_code=401, detail="Missing key",
                    headers={"WWW-Authenticate": "Bearer"})
```

## An error deep down: your own exception class

The place where an error happens is often not the endpoint itself but a
function it calls. That function doesn't need to know about HTTP:

```python
class OutOfStock(Exception):
    def __init__(self, item: str):
        self.item = item


def take(item: str):
    if stock[item] == 0:
        raise OutOfStock(item)
    stock[item] -= 1
```

`take` is an ordinary Python function; it could be used in another program
too. You write a handler that turns this exception into an HTTP answer
**once**:

```python
from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(OutOfStock)
def out_of_stock_handler(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=409,
                        content={"error": "out_of_stock", "item": exc.item})


@app.post("/buy/{item}")
def buy(item: str):
    take(item)
    return {"item": item, "left": stock[item]}
```

```text
POST /buy/pen    200 {"item": "pen", "left": 2}
POST /buy/book   409 {"error": "out_of_stock", "item": "book"}
```

No matter which endpoint raises `OutOfStock`, or how deep, it turns into the
same answer.

<figure class="fig">
  <div class="flow">
    <span class="node">buy()</span><span class="arrow">→</span>
    <span class="node no">take()<br><small>raise OutOfStock</small></span><span class="arrow">→</span>
    <span class="node acc">exception_handler</span><span class="arrow">→</span>
    <span class="node ok">409 JSON</span>
  </div>
  <figcaption>The exception travels up from the deep function; the handler turns it into an HTTP answer in one place.</figcaption>
</figure>

## Changing the 422's format

FastAPI's validation error is an exception too: `RequestValidationError`.
You can catch it and turn it into your own format:

```python
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
def validation_handler(request: Request, exc: RequestValidationError):
    fields = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422,
                        content={"error": "invalid_input", "fields": fields})
```

```text
GET /n?x=abc   422 {"error": "invalid_input", "fields": ["x"]}
```

`exc.errors()` is the `detail` list you know; `loc[1:]` drops the first item
(`query`, `body`) and leaves the field name. If you do this, use the same
format across the whole API: the client should read errors from the same
place at every endpoint.

## Unexpected errors

An uncaught error like `1 / 0` returns the plain text `500 Internal Server
Error`. A handler can turn this into JSON too:

```python
@app.exception_handler(Exception)
def unexpected(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal"})
```

```text
GET /boom   500 {"error": "internal"}
```

One difference: even though this handler sends the answer, the error is
**still** written to the server log and is raised as an exception in tests
(we measured). That's a good thing: a `500` is a bug and needs to be seen.
**Don't send the error's details to the client**; `str(exc)` leaks your
code's insides (file paths, queries).

## Summary

- `raise HTTPException(status_code=..., detail=..., headers=...)`.
- `detail` can be a dictionary; put a fixed `code` for programs to read.
- Your own exception class + `@app.exception_handler(Class)`: the error deep
  down, the translation in one place.
- Catching `RequestValidationError` changes the `422`'s format.
- For unexpected errors, give the client no details; they stay in the log.
