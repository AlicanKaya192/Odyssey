# Bağımlılıklar

API büyüdükçe aynı satırlar uç noktadan uç noktaya kopyalanmaya başlar:
sayfalama parametreleri, "kaydı bul ya da 404", anahtar denetimi,
veritabanı bağlantısını açıp kapatmak. FastAPI'nin bunun için bir aracı
var: **bağımlılık** (dependency). Bir kez yazılan bir işlevi, uç noktalara
"bunu önce çalıştır, sonucunu bana ver" diye bağlarsın.

## İlk bağımlılık: sayfalama

`/books` ve `/authors` ikisi de `limit` ve `offset` alsın. Kuralları iki
kez yazmak yerine:

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

app = FastAPI()


def paging(limit: Annotated[int, Query(ge=1, le=50)] = 10,
           offset: Annotated[int, Query(ge=0)] = 0):
    return {"limit": limit, "offset": offset}


@app.get("/books")
def list_books(page: Annotated[dict, Depends(paging)]):
    items = list(books.values())
    return items[page["offset"]:page["offset"] + page["limit"]]


@app.get("/authors")
def list_authors(page: Annotated[dict, Depends(paging)]):
    return {"page": page}
```

- `paging` sıradan bir işlev. Parametreleri uç noktanınkiler gibi okunuyor:
  burada sorgudan.
- `Depends(paging)`: "bu parametrenin değeri `paging`'in döndürdüğü olsun".
- `paging`'deki kurallar her iki uç noktada da geçerli.

```text
GET /books?limit=2      200 [{"title": "Dune"}, {"title": "Emma"}]
GET /books?limit=99     422 less_than_equal, loc ["query", "limit"]
GET /authors?offset=5   200 {"page": {"limit": 10, "offset": 5}}
```

`/docs` da `limit` ve `offset`'i her iki uç noktada, kurallarıyla
gösteriyor: bağımlılığın parametreleri uç noktanın parametresi sayılıyor.

## Kısaltma: tipe ad vermek

`Annotated[dict, Depends(paging)]` uzun. Bir kez ad verip her yerde
kullanabilirsin:

```python
Paging = Annotated[dict, Depends(paging)]


@app.get("/books")
def list_books(page: Paging):
    ...
```

<figure class="fig">
  <div class="flow">
    <span class="node">GET /books?limit=2</span><span class="arrow">→</span>
    <span class="node acc">paging()<br><small>limit, offset denetlenir</small></span><span class="arrow">→</span>
    <span class="node">page = {"limit": 2, "offset": 0}</span><span class="arrow">→</span>
    <span class="node ok">list_books(page)</span>
  </div>
  <figcaption>FastAPI önce bağımlılığı çalıştırıyor, sonucunu uç noktaya parametre olarak veriyor. Bağımlılık hata fırlatırsa uç nokta hiç çalışmıyor.</figcaption>
</figure>

## Bulamazsan 404, bağımlılık olarak

CRUD bölümündeki `find_book` yardımcısı da bağımlılık olabilir:

```python
def get_book(book_id: int) -> dict:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.get("/books/{book_id}")
def read_book(book: Annotated[dict, Depends(get_book)]):
    return book
```

`get_book`'un `book_id` parametresi adresteki `{book_id}`'den doldu. Kitap
yoksa bağımlılık `HTTPException` fırlatıyor ve uç nokta **hiç
çalışmıyor**: `GET /books/9` → `404`. Uç noktanın kendisi artık "kitap
kesin var" diye yazılabiliyor.

## Bağımlılığın bağımlılığı

Bir bağımlılık başka bir bağımlılık isteyebilir; FastAPI zinciri kendisi
çözer. Aynı bağımlılık bir istekte birden fazla yerde istense de **bir kez**
çalışır ve sonucu paylaşılır. Ölçtük: bir sayaç bağımlılığını hem doğrudan
hem başka bir bağımlılığın içinden istedik, sayaç bir kez arttı
(`{"a": 1, "b": 1, "calls": 1}`).

## Sonucu olmayan bağımlılık: denetim

Bazen bağımlılığın döndürdüğü değer gerekmez; yalnızca **çalışması**
gerekir. Örneğin bir anahtar denetimi:

```python
from fastapi import Header


def require_key(x_key: Annotated[str | None, Header()] = None):
    if x_key != "secret":
        raise HTTPException(status_code=401, detail="Bad key")


@app.get("/admin", dependencies=[Depends(require_key)])
def admin():
    return {"ok": True}
```

- `Header()`: değer bir başlıktan okunuyor. Parametre adı `x_key`,
  başlığın adı `X-Key` (alt çizgi tireye, büyük/küçük harf fark etmez).
- `dependencies=[...]` dekoratörde: işlev parametre olarak almıyor ama
  bağımlılık çalışıyor.

```text
GET /admin                   401 {"detail": "Bad key"}
GET /admin  (X-Key: secret)  200 {"ok": true}
```

Kimlik doğrulamanın bütünü bir sonraki bölümde.

## Aç ve kapat: `yield`

Bazı kaynaklar istekten önce açılıp istekten sonra kapatılmalı: veritabanı
bağlantısı, dosya. `return` yerine `yield` kullanan bağımlılık:

```python
def get_session():
    session = open_session()       # istekten önce
    try:
        yield session              # uç nokta bunu alır
    finally:
        session.close()            # cevaptan sonra, hata olsa da
```

Ölçtük: `yield`'den önceki kısım uç noktadan önce, `finally` içindeki kısım
cevap gönderildikten **sonra** çalıştı. `try/finally` sayesinde uç noktada
hata çıksa da kapanış yapılıyor. Veritabanı bölümünde gerçek bir SQLite
bağlantısıyla kullanacaksın.

## Testte değiştirmek

Bağımlılığın bir faydası daha var: testte onu başka bir işlevle
değiştirebilirsin.

```python
app.dependency_overrides[paging] = lambda: {"limit": 1, "offset": 0}
```

Bundan sonra `GET /books` tek kitap döndürdü (ölçtük). Gerçek veritabanı
yerine sahte bir tane, gerçek anahtar denetimi yerine "her zaman geçer"
vermek için kullanılır; Test bölümünde ayrıntısı var.

## Özet

- Bağımlılık sıradan bir işlev; `Depends(işlev)` ile parametreye bağlanır.
- Parametreleri (sorgu, yol, başlık) uç noktanınki gibi okunur ve
  belgeye girer.
- `HTTPException` fırlatırsa uç nokta çalışmaz.
- Sonucu gerekmiyorsa `dependencies=[Depends(...)]`.
- `yield`'li bağımlılık: önce aç, cevaptan sonra kapat (`try/finally`).
- Bir istekte aynı bağımlılık bir kez çalışır; testte
  `app.dependency_overrides` ile değiştirilir.
