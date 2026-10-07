# Dosya Düzeni: Router'lar

Şimdiye kadar bütün API tek bir `main.py`'deydi. Kitaplar, kullanıcılar,
yönetici sayfası, modeller, bağımlılıklar... Bir noktada dosya yüzlerce
satır olur ve aradığını bulamazsın. Bu bölümde API'yi **dosyalara**
bölüyorsun.

## Hedef düzen

```text
main.py            uygulama: router'ları bir araya getirir
models.py          Pydantic modelleri
deps.py            ortak bağımlılıklar (anahtar, veritabanı)
routers/
    __init__.py    boş: "bu klasör bir paket" demek
    books.py       /books uç noktaları
    admin.py       /admin uç noktaları
```

Python patikasındaki modüller bölümünü hatırla: her `.py` dosyası bir
modül, `import` ile başka dosyadan kullanılıyor. `routers/` klasörünün
içindeki `__init__.py` onu bir **paket** yapıyor; böylece
`from routers import books` yazılabiliyor.

## `APIRouter`: küçük bir `app`

`routers/books.py`:

```python
from fastapi import APIRouter, HTTPException

from models import Book

router = APIRouter(prefix="/books", tags=["books"])
books = {1: {"title": "Dune", "year": 1965}}


@router.get("")
def list_books():
    return books


@router.get("/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@router.post("", status_code=201)
def add_book(book: Book):
    ...
```

- `APIRouter` uç noktaları `app` gibi topluyor ama kendi başına
  çalışmıyor; bir uygulamaya **eklenmesi** gerekiyor.
- `prefix="/books"`: bu dosyadaki her adresin başına ekleniyor.
  `@router.get("/{book_id}")` gerçekte `/books/{book_id}`.
- `@router.get("")`: yalnızca önek, yani `/books`.
- `tags=["books"]`: `/docs`'ta bu uç noktalar "books" başlığı altında
  toplanıyor.

## `main.py`: bir araya getirmek

```python
from fastapi import FastAPI

from routers import admin, books

app = FastAPI(title="Library")
app.include_router(books.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"name": "Library"}
```

`include_router` router'ın bütün uç noktalarını uygulamaya ekliyor. Ölçtük:

```text
GET /books        200 {"1": {"title": "Dune", "year": 1965}}
GET /books/1      200 {"title": "Dune", "year": 1965}
GET /books/7      404 {"detail": "Book not found"}
POST /books       201 {"id": 2, "title": "Emma", "year": 1815}
GET /             200 {"name": "Library"}
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">main.py<br><small>app + include_router</small></span><span class="arrow">→</span>
    <span class="node">routers/books.py<br><small>prefix /books</small></span><span class="arrow">→</span>
    <span class="node">models.py · deps.py</span>
  </div>
  <figcaption>İçe aktarma tek yönde: <code>main</code> router'ları, router'lar modelleri ve bağımlılıkları içe aktarıyor. Tersi döngü yaratır.</figcaption>
</figure>

## Router'a toplu bağımlılık

Yönetici uç noktalarının **hepsi** anahtar istesin. Her birine
`dependencies=` yazmak yerine router'a bir kez:

```python
# deps.py
def require_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "letmein":
        raise HTTPException(status_code=401, detail="Invalid API key")
```

```python
# routers/admin.py
from fastapi import APIRouter, Depends

from deps import require_key

router = APIRouter(prefix="/admin", tags=["admin"],
                   dependencies=[Depends(require_key)])


@router.get("/stats")
def stats():
    return {"books": 1}
```

```text
GET /admin/stats                       401 {"detail": "Invalid API key"}
GET /admin/stats  (X-Api-Key: letmein) 200 {"books": 1}
```

Bu router'a eklenen her yeni uç nokta kendiliğinden korunuyor; unutma
ihtimali kalmıyor.

## Sondaki eğik çizgi

Önek `/books` ve uç nokta `""` ise adres `/books`. `GET /books/` (sonda `/`)
gönderilince FastAPI `307` ile `/books`'a yönlendiriyor (ölçtük). Tarayıcı
ve `requests` yönlendirmeyi kendiliğinden izliyor, ama bir `POST` gövdesi
yönlendirmede kaybolabilir. Adresleri belgede nasılsa öyle yaz.

## Neyi nereye koymalı?

| Dosya | İçinde | İçe aktarır |
|---|---|---|
| `models.py` | Pydantic modelleri | Yalnızca `pydantic` |
| `deps.py` | `get_db`, `require_key`, `current_user` | `fastapi`, veritabanı |
| `routers/*.py` | Uç noktalar | `models`, `deps` |
| `main.py` | `app`, `include_router` | `routers` |

Ok tek yöne gidiyor: `main` → `routers` → `models`, `deps`. Tersine
`import` yazarsan (örneğin `models.py` içinde `from main import app`)
**döngüsel içe aktarma** olur ve program açılmaz.

## Özet

- `APIRouter(prefix=..., tags=...)` bir dosyanın uç noktalarını toplar.
- `app.include_router(router)` onları uygulamaya ekler.
- Router'a `dependencies=[...]`: içindeki her uç nokta korunur.
- `routers/__init__.py` klasörü paket yapar.
- İçe aktarma tek yönlü: `main` → `routers` → `models`/`deps`.
