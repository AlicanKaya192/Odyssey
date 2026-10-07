What's inside `/openapi.json`, and which part of the code goes where.

## The main parts

```text
{
  "openapi": "3.1.0",
  "info": {...},          FastAPI(title=, version=, description=)
  "paths": {...},         the endpoints
  "components": {
    "schemas": {...}      Pydantic models
  }
}
```

## An endpoint's entry

Inside `paths["/books/{book_id}"]["get"]` (we measured):

| Field | From where? |
|---|---|
| `tags` | `tags=["books"]` |
| `summary` | `summary=` (otherwise from the function name: `add_book` → `"Add Book"`) |
| `description` | The function's docstring |
| `operationId` | Function name + address + method: `add_book_books_post` |
| `parameters` | Path, query and header parameters with their rules |
| `requestBody` | The body model |
| `responses` | `200` + `422` + those you added with `responses=` |
| `deprecated` | `deprecated=True` |

An endpoint with `include_in_schema=False` isn't in `paths` at all.

## A model's entry

`components.schemas.Book` (we measured):

```json
{"properties": {
   "title": {"type": "string", "title": "Title", "examples": ["Dune"]},
   "year": {"type": "integer", "title": "Year",
            "description": "Year of first publication", "examples": [1965]}},
 "type": "object", "required": ["title", "year"], "title": "Book"}
```

Rules like `Field(ge=1450)` show up here too, as `minimum`.

## Turning the docs off

`FastAPI(docs_url=None, redoc_url=None)`: `/docs` and `/redoc` give `404`, but
`/openapi.json` is still `200` (we measured). To turn that off too,
`openapi_url=None`. Leaving the docs open is usually fine; secrets are
protected by identity checks, not by hiding an endpoint's name.
