The same resource has several models. To avoid writing fields again, they
inherit from a shared base model.

```python
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserIn(UserBase):      # what the client sends
    password: str


class UserOut(UserBase):     # what goes to the client
    id: int
```

- `UserIn`: `name`, `email`, `password`. The `POST` body.
- `UserOut`: `name`, `email`, `id`. The answer; no password at all.

We measured: an endpoint taking `UserIn` and returning `-> UserOut` gave
`{"name": "Ada", "email": "a@x.org", "id": 1}`. Field order: the base
model's first, then the added ones. A body without the password is `422`
(`loc: ["body", "password"]`).

## Naming

| Model | For what? |
|---|---|
| `XBase` | Shared fields; not used directly |
| `XIn` / `XCreate` | The body when creating |
| `XUpdate` | The body when updating (fields usually optional) |
| `XOut` / `X` | The answer |

## In `/docs`

The response model goes into the docs too: opening `GET /users/{user_id}`
shows the `UserOut` schema under "Responses". In the OpenAPI entry of a
function written with `-> UserOut`, the response schema is
`#/components/schemas/UserOut` (we measured). So whoever writes the client
knows the answer's shape without reading the code.

## When `response_model`, when `-> Model`?

Both do the same job. `-> Model` is shorter and the editor understands it
too. `response_model=` is needed when:

- The function returns a dictionary and the editor warns "this dictionary
  isn't a `UserOut`".
- You'll write extra settings like `response_model_exclude_none=True`.
