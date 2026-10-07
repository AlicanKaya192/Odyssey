`/openapi.json`'ın içinde ne var ve kodun hangi parçası nereye gidiyor.

## Ana parçalar

```text
{
  "openapi": "3.1.0",
  "info": {...},          FastAPI(title=, version=, description=)
  "paths": {...},         uç noktalar
  "components": {
    "schemas": {...}      Pydantic modelleri
  }
}
```

## Bir uç noktanın kaydı

`paths["/books/{book_id}"]["get"]` içinde (ölçtük):

| Alan | Nereden? |
|---|---|
| `tags` | `tags=["books"]` |
| `summary` | `summary=` (yoksa işlev adından: `add_book` → `"Add Book"`) |
| `description` | İşlevin docstring'i |
| `operationId` | İşlev adı + adres + yöntem: `add_book_books_post` |
| `parameters` | Yol, sorgu, başlık parametreleri ve kuralları |
| `requestBody` | Gövde modeli |
| `responses` | `200` + `422` + `responses=` ile eklediklerin |
| `deprecated` | `deprecated=True` |

`include_in_schema=False` olan uç nokta `paths`'te hiç yok.

## Bir modelin kaydı

`components.schemas.Book` (ölçtük):

```json
{"properties": {
   "title": {"type": "string", "title": "Title", "examples": ["Dune"]},
   "year": {"type": "integer", "title": "Year",
            "description": "Year of first publication", "examples": [1965]}},
 "type": "object", "required": ["title", "year"], "title": "Book"}
```

`Field(ge=1450)` gibi kurallar da burada `minimum` olarak görünür.

## Belgeyi kapatmak

`FastAPI(docs_url=None, redoc_url=None)`: `/docs` ve `/redoc` `404`, ama
`/openapi.json` yine `200` (ölçtük). Onu da kapatmak için
`openapi_url=None`. Belgeyi açık bırakmak çoğu zaman iyidir; gizli bir şey
uç noktanın adında değil, kimlik denetiminde korunur.
