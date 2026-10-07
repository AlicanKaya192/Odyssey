# Response Models and Status Codes

Until now you put a template on **incoming** data. This section is the
other direction: the **outgoing** answer. Two questions: which fields will
be in the answer (the response model), and what will its status code be.

## The problem: not everything inside should go out

Think of an API that keeps user records. The record has a password too:

```python
users[1] = {"id": 1, "name": "Ada", "password": "secret"}
```

If you write `return users[1]`, the password goes into the answer as well.
Deleting fields by hand in every endpoint is easy to forget. The solution:
describe the answer's template with a model too.

## The response model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = {}


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str


@app.post("/users", status_code=201, response_model=UserOut)
def create_user(user: UserIn):
    new_id = len(users) + 1
    users[new_id] = {"id": new_id, **user.model_dump()}
    return users[new_id]
```

The function returns the dictionary with the password, but the answer is:

```text
POST /users  {"name": "Ada", "password": "secret"}
201          {"id": 1, "name": "Ada"}
```

`response_model=UserOut`: FastAPI passes the returned value through this
model; fields not in the model (`password`) are **dropped**. That's why
writing two separate models for input and output (`UserIn` / `UserOut`)
is common.

<figure class="fig">
  <div class="flow">
    <span class="node">Incoming body<br><small>name, password</small></span><span class="arrow">→</span>
    <span class="node acc">UserIn</span><span class="arrow">→</span>
    <span class="node">Your function<br><small>record: id, name, password</small></span><span class="arrow">→</span>
    <span class="node acc">UserOut</span><span class="arrow">→</span>
    <span class="node ok">Answer<br><small>id, name</small></span>
  </div>
  <figcaption>The input model filters the incoming body, the response model filters the outgoing answer. The password stays in the record but doesn't get out, because it isn't in <code>UserOut</code>.</figcaption>
</figure>

## A return type works too

The same thing can be written with the function's return type:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int) -> UserOut:
    return users[user_id]
```

`-> UserOut` → the answer is `{"id": 1, "name": "Ada"}`. Extra fields are
dropped here too (we measured: we returned a dictionary with `password`
and `admin`, neither went out). For a list, `-> list[UserOut]` or
`response_model=list[UserOut]`.

## The response model checks you too

If the value you return **doesn't fit** the model, the mistake is yours,
not the client's:

```python
@app.get("/bad", response_model=UserOut)
def bad():
    return {"name": "Ada"}          # no id
```

```text
GET /bad   500 Internal Server Error
```

The server's log says why:

```text
ResponseValidationError: 1 validation error:
  {'type': 'missing', 'loc': ('response', 'id'), 'msg': 'Field required', ...}
```

This time `loc` starts with `response`. The client didn't send anything
wrong; `500` means "there is a bug on the server".

## Status codes

The answer's first line lets the client understand the result without
reading the body. The codes you read in API 1 are **your choice** here:

| Status | When? |
|---|---|
| `200 OK` | The default; reading, updating |
| `201 Created` | A new record was created (`POST`) |
| `204 No Content` | Success, but there's no body to send (`DELETE`) |
| `400 Bad Request` | The request fits the rules but can't be processed |
| `404 Not Found` | No such record |
| `409 Conflict` | A clash: the same name already exists |
| `422 Unprocessable Content` | Validation failed (FastAPI itself) |

You don't have to memorise the numbers; the `status` module has them by
name:

```python
from fastapi import status


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    users.pop(user_id, None)
```

```text
DELETE /users/1   204   (no body)
```

A `204` sends no body: even when the function returned something, the
answer went out empty (we measured).

## Deciding the code at that moment

`status_code=201` in the decorator is fixed. Sometimes the code depends on
the situation; then you return a `JSONResponse`:

```python
from fastapi.responses import JSONResponse


@app.post("/jobs")
def start_job():
    return JSONResponse(status_code=202, content={"queued": True})
```

A `JSONResponse` goes out **as it is**: `response_model` doesn't filter it.
For error cases the next step is `HTTPException` (the Error Responses
section).

## Adding a header

Giving the new record's address in a `Location` header is a good habit.
Ask for a `Response` parameter and write the header on it:

```python
from fastapi import Response


@app.post("/users", status_code=201)
def create_user(user: UserIn, response: Response):
    ...
    response.headers["Location"] = f"/users/{new_id}"
    return {...}
```

```text
201   location: /users/7
```

## Skipping `null` fields

```python
@app.get("/book", response_model=Book, response_model_exclude_none=True)
def book():
    return {"title": "Dune", "note": None}
```

The answer is `{"title": "Dune"}`: `note`, whose value is `None`, wasn't
written at all.

## Summary

- `response_model=Model` or `-> Model`: the answer's template; extra fields
  are dropped, a missing field is `500` (`ResponseValidationError`).
- Separate models for input and output: `UserIn` (with the password),
  `UserOut` (without).
- `status_code=` in the decorator; by name, `status.HTTP_201_CREATED`.
- `204` has no body; for a decision on the spot, `JSONResponse(status_code=...)`.
- For a header, a `response: Response` parameter.
