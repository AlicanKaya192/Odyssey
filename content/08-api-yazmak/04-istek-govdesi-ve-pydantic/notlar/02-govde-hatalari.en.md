The kinds of `422` answers that come from the body and what they mean.
`loc` always starts with `body`; the next item is the field's name (in a
nested model the path: `["body", "author", "name"]`, in a list the position:
`["body", "items", 0, "price"]`).

| `type` | Example body | Meaning |
|---|---|---|
| `missing` | `{"title": "Dune"}` | A required field is missing (`year`) |
| `missing` (`loc: ["body"]`) | no body | No body was sent at all |
| `int_parsing` | `{"year": "nineteen"}` | Could not become a number |
| `int_from_float` | `{"year": 1965.5}` | A fractional number cannot be an integer |
| `string_type` | `{"title": 5}` | Text was expected |
| `list_type` | `{"tags": "sf"}` | A list was expected |
| `model_attributes_type` | `{"author": "Austen"}` | An object was expected |
| `json_invalid` | `{bad json` | The JSON could not be read at all |

## While debugging

1. First `loc`: which field?
2. Then `type` and `msg`: what was expected?
3. `input`: what came? Usually a typo or a quote mistake.

On the client side (`requests`) the most common cause: using `data=` instead
of `json=`. `data=` sends the body as a form (`title=Dune&year=1965`);
because FastAPI expects a JSON object, `422` comes back: `type:
model_attributes_type`, `loc: ["body"]` (measured).

## Extra fields

Fields that are not in the model are dropped without an error. If you want
to catch a client writing a wrong field name, add this line to the model:

```python
from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    year: int
```

Then `{"title": "Dune", "year": 1965, "yaer": 1}` → `422`
(`extra_forbidden`).
