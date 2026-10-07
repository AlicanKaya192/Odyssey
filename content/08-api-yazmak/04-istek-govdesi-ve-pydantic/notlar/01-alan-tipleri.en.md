Field types often used in a Pydantic model and what they accept
(measured; Pydantic 2.13).

| Field | Accepts | Rejects |
|---|---|---|
| `title: str` | `"Dune"` | `5` (does not turn a number into text) |
| `year: int` | `1965`, `"1965"` | `1965.5`, `"nineteen"` |
| `price: float` | `9.5`, `9`, `"9.5"` | `"cheap"` |
| `active: bool` | `true`, `false`, `"true"`, `1`, `0` | `"maybe"` |
| `tags: list[str]` | `["a", "b"]` | `"a"` (not a list) |
| `extra: dict[str, int]` | `{"a": 1}` | `{"a": "x"}` |
| `author: Author` | `{"name": "Austen"}` | `"Austen"` |
| `items: list[Item]` | `[{"name": "pen", "price": 1.5}]` | a list whose item does not fit |

## Required and optional

```python
class Book(BaseModel):
    title: str                  # required
    year: int                   # required
    tags: list[str] = []        # optional, default []
    note: str | None = None     # optional, default null
    pages: int = 0              # optional, default 0
```

## Working with a model

| Code | Result |
|---|---|
| `book.title` | The field's value |
| `book.model_dump()` | A `{"title": ..., "year": ..., ...}` dictionary |
| `book.model_dump(exclude_none=True)` | Without the fields that are `None` |
| `{"id": 3, **book.model_dump()}` | Adding a new key to the dictionary |
| `Book(title="Dune", year=1965)` | Creating a model in code |
| `return book` | FastAPI turns it into JSON |

## A reminder from the Python track

`class Book(BaseModel):` is a class definition; it **inherits** from
`BaseModel` (the Object-Oriented Programming section). You do not need to write `__init__`:
Pydantic builds it from the field list. Field names are English and
lowercase (`title`, `year`); they must match the keys in the JSON exactly.
