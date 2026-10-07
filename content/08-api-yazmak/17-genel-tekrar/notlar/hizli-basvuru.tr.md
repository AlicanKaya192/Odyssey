Patikanın bütün kalıpları tek sayfada.

## Uygulama ve uç nokta

```python
from fastapi import FastAPI

app = FastAPI(title="Library API", version="1.0.0")


@app.get("/books/{book_id}")
def read_book(book_id: int, full: bool = False):
    ...
```

| Yazım | Anlamı |
|---|---|
| `{book_id}` adreste | Yol parametresi |
| `full: bool = False` | İsteğe bağlı sorgu |
| `book: Book` (model) | Gövde |
| `Annotated[int, Query(ge=1)]` | Kurallı sorgu |
| `Annotated[str, Header()]` | Başlık |

## Model ve doğrulama

```python
from pydantic import BaseModel, Field, field_validator


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1450, le=2100)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()
```

## Cevap

| Yazım | Ne yapar? |
|---|---|
| `status_code=201` | Başarı kodu |
| `-> BookOut` / `response_model=BookOut` | Cevabı süzer |
| `raise HTTPException(404, detail="...")` | Hata cevabı |
| `JSONResponse(status_code=202, content={...})` | Anlık kod |
| `response.headers["Location"] = ...` | Başlık |

## Bağımlılık ve kimlik

```python
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    ...
```

## Veritabanı

| Yazım | Ne yapar? |
|---|---|
| `db.execute("... WHERE id = ?", (book_id,))` | Parametreli sorgu |
| `.fetchone()` / `.fetchall()` | Satır / satırlar |
| `db.commit()` | Kalıcı yap |
| `cur.lastrowid` / `cur.rowcount` | Yeni numara / etkilenen satır |

## Düzen, test, çalıştırma

| Yazım | Ne yapar? |
|---|---|
| `APIRouter(prefix="/books", tags=["books"])` | Dosyaya özel router |
| `app.include_router(books.router)` | Router'ı ekle |
| `client = TestClient(app)` | Testte istemci |
| `@pytest.fixture(autouse=True)` | Her testten önce |
| `uvicorn main:app --reload` | Geliştirirken çalıştır |

## Durum kodları

`200` tamam · `201` oluşturuldu · `204` gövdesiz · `400` mantıksız istek ·
`401` kimlik yok · `403` izin yok · `404` bulunamadı · `409` çakışma ·
`422` doğrulama · `500` sunucu hatası
