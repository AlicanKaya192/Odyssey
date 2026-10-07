What you need to know about `field_validator` and `model_validator`, all
measured.

## `mode="after"` and `mode="before"`

The default is `after`: the function runs **after** the type check, so the
value already has the right type. `before` receives the raw value; it is
used to bend incoming data into the type:

```python
class Post(BaseModel):
    tags: list[str] = []

    @field_validator("tags", mode="before")
    @classmethod
    def split(cls, value):
        if isinstance(value, str):
            return [t.strip() for t in value.split(",")]
        return value
```

`{"tags": "sf, classic"}` → `{"tags": ["sf", "classic"]}`; a list passes
through as it is.

## Looking at another field

A field validator sees the fields defined **before** it in `info.data`:

```python
class Range(BaseModel):
    a: int
    b: int

    @field_validator("b")
    @classmethod
    def b_after_a(cls, value, info):
        if "a" in info.data and value <= info.data["a"]:
            raise ValueError("b must be greater than a")
        return value
```

`{"a": 5, "b": 3}` → `422`, `loc: ["body", "b"]`. If `a` itself is broken
(`"x"`) it is not in `info.data`; that's why the `"a" in info.data` check
is there. For two-field rules `model_validator(mode="after")` is usually
more readable.

## Common mistakes

All measured; the first three produce a wrong result **without an error**,
which is what makes them dangerous:

| Mistake | Result |
|---|---|
| Forgot `return value` | `200`, the field's value is `null` |
| Forgot `return self` in `model_validator` | `200`, the answer is just `null` |
| `return False` instead of `raise ValueError` | `200`, the field's value is `false` |
| Misspelt field name (`"usernme"`) | `PydanticUserError` when the program starts |

## The message

`raise ValueError("must not contain spaces")` → `msg`:
`"Value error, must not contain spaces"`. Pydantic adds `Value error, ` at
the front. Write the message for the client to read: short, in English.
