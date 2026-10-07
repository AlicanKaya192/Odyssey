Pydantic modelinde sık kullanılan alan tipleri ve neyi kabul ettikleri
(ölçüldü; Pydantic 2.13).

| Alan | Kabul eder | Reddeder |
|---|---|---|
| `title: str` | `"Dune"` | `5` (sayıyı metne çevirmez) |
| `year: int` | `1965`, `"1965"` | `1965.5`, `"nineteen"` |
| `price: float` | `9.5`, `9`, `"9.5"` | `"cheap"` |
| `active: bool` | `true`, `false`, `"true"`, `1`, `0` | `"maybe"` |
| `tags: list[str]` | `["a", "b"]` | `"a"` (liste değil) |
| `extra: dict[str, int]` | `{"a": 1}` | `{"a": "x"}` |
| `author: Author` | `{"name": "Austen"}` | `"Austen"` |
| `items: list[Item]` | `[{"name": "pen", "price": 1.5}]` | öğesi kalıba uymayan liste |

## Zorunlu ve isteğe bağlı

```python
class Book(BaseModel):
    title: str                  # zorunlu
    year: int                   # zorunlu
    tags: list[str] = []        # isteğe bağlı, varsayılan []
    note: str | None = None     # isteğe bağlı, varsayılan null
    pages: int = 0              # isteğe bağlı, varsayılan 0
```

## Modelle çalışmak

| Yazım | Sonuç |
|---|---|
| `book.title` | Alanın değeri |
| `book.model_dump()` | `{"title": ..., "year": ..., ...}` sözlüğü |
| `book.model_dump(exclude_none=True)` | `None` olan alanlar olmadan |
| `{"id": 3, **book.model_dump()}` | Sözlüğe yeni anahtar ekleyerek |
| `Book(title="Dune", year=1965)` | Kodda model oluşturmak |
| `return book` | FastAPI JSON'a çevirir |

## Python patikasından hatırlatma

`class Book(BaseModel):` bir sınıf tanımı; `BaseModel`'den **kalıtım**
alıyor (Nesne Tabanlı Programlama bölümü). `__init__` yazmana gerek yok: Pydantic alan
listesinden kendisi kuruyor. Alan adları İngilizce ve küçük harf
(`title`, `year`); JSON'daki anahtarlarla birebir aynı olmalı.
