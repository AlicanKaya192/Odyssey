# CRUD: Tam Bir Kaynak

Şimdiye kadar parçaları tek tek yazdın: yol, sorgu, gövde, doğrulama, yanıt
modeli, durum kodları. Bu bölümde hepsini bir araya getirip **tam bir
kaynak** yazıyorsun: kitap ekleme, listeleme, okuma, değiştirme, silme.
Bu beş işe kısaca **CRUD** denir.

## CRUD ve HTTP yöntemleri

| İş | İngilizcesi | Yöntem | Adres | Başarılı kod |
|---|---|---|---|---|
| Oluştur | **C**reate | `POST` | `/books` | `201` |
| Listele | **R**ead | `GET` | `/books` | `200` |
| Birini oku | **R**ead | `GET` | `/books/{id}` | `200` |
| Tamamını değiştir | **U**pdate | `PUT` | `/books/{id}` | `200` |
| Bir kısmını değiştir | **U**pdate | `PATCH` | `/books/{id}` | `200` |
| Sil | **D**elete | `DELETE` | `/books/{id}` | `204` |

İki adres yetiyor: koleksiyon (`/books`) ve tek kayıt (`/books/{id}`).
Ne yapılacağını yöntem söylüyor. API 1'de istemci olarak kullandığın düzen
buydu; şimdi sunucusunu yazıyorsun.

<figure class="fig">
  <div class="versus">
    <div><h4>/books (koleksiyon)</h4><p><code>POST</code> → yeni kitap, <code>201</code><br><code>GET</code> → liste, <code>200</code></p></div>
    <div><h4>/books/{id} (tek kayıt)</h4><p><code>GET</code> → kitap ya da <code>404</code><br><code>PUT</code> / <code>PATCH</code> → değiştir<br><code>DELETE</code> → sil, <code>204</code></p></div>
  </div>
  <figcaption>İki adres, beş yöntem. Adres neyin üzerinde çalışıldığını, yöntem ne yapıldığını söylüyor.</figcaption>
</figure>

## Modeller

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1


class BookIn(BaseModel):
    title: str = Field(min_length=1)
    year: int


class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    year: int | None = None


class BookOut(BookIn):
    id: int
```

- `BookIn`: oluştururken ve `PUT`'ta gelen gövde; iki alan da zorunlu.
- `BookPatch`: `PATCH` gövdesi; **her alan isteğe bağlı**, çünkü kişi
  yalnızca değiştirmek istediğini gönderir.
- `BookOut`: cevap; `BookIn`'in alanları + `id`.

## Kimlik numarası: `len()` tuzağı

İlk akla gelen `new_id = len(books) + 1`. Ölçtük:

```text
POST /books  A      201 {"id": 1}
POST /books  B      201 {"id": 2}
DELETE /books/1     204
POST /books  C      201 {"id": 2}     ← B'nin numarası!
GET /books          {"2": C}          ← B kayboldu
```

Silmeden sonra kayıt sayısı azalıyor ve yeni kayıt var olanın üstüne
yazılıyor. Çözüm: hiç geri gitmeyen bir sayaç.

```python
@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookIn) -> BookOut:
    global next_id
    record = {"id": next_id, **book.model_dump()}
    books[next_id] = record
    next_id += 1
    return record
```

`global next_id`: işlevin içinde modüldeki `next_id`'yi **değiştireceğimizi**
söylüyor; yazılmazsa Python onu işlevin kendi değişkeni sanıp
`UnboundLocalError` verir. (Veritabanı bölümünde bu işi veritabanı
yapacak.)

## Bulamazsan 404: ortak yardımcı

Okuma, değiştirme ve silmenin üçü de önce kaydı bulmalı. Aynı `if`'i üç kez
yazmamak için:

```python
def find_book(book_id: int) -> dict:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
```

`raise HTTPException(...)` işlevi orada durdurup hata cevabını gönderiyor;
yardımcının içinden fırlatılsa da çalışıyor. Ayrıntısı bir sonraki
bölümde.

## Okumak ve listelemek

```python
@app.get("/books")
def list_books(year: int | None = None) -> list[BookOut]:
    result = list(books.values())
    if year is not None:
        result = [b for b in result if b["year"] == year]
    return result


@app.get("/books/{book_id}")
def read_book(book_id: int) -> BookOut:
    return find_book(book_id)
```

Listeleme isteğe bağlı bir süzgeç alıyor: `GET /books?year=1815`.

## `PUT`: tamamını değiştir

```python
@app.put("/books/{book_id}")
def replace_book(book_id: int, book: BookIn) -> BookOut:
    find_book(book_id)
    books[book_id] = {"id": book_id, **book.model_dump()}
    return books[book_id]
```

`PUT` kaydın **tamamını** gönderilenle değiştirir; bu yüzden `BookIn`
alıyor ve eksik alan `422`:

```text
PUT /books/2  {"title": "Persuasion", "year": 1817}   200
PUT /books/2  {"title": "Persuasion"}                 422 missing year
```

## `PATCH`: yalnızca gönderileni değiştir

```python
@app.patch("/books/{book_id}")
def update_book(book_id: int, patch: BookPatch) -> BookOut:
    record = find_book(book_id)
    record.update(patch.model_dump(exclude_unset=True))
    return record
```

Püf noktası `exclude_unset=True`. `{"year": 1966}` gönderilince:

```text
patch.model_dump()                    {"title": None, "year": 1966}
patch.model_dump(exclude_unset=True)  {"year": 1966}
```

`exclude_unset` olmasa başlık `None`'a dönerdi. Bu seçenek "istemcinin
**gönderdiği**" alanları veriyor; gönderilmeyenle bilerek `null`
gönderileni ayırıyor.

### Gönderilen `null`

Ölçerken bir hata yakaladık: `PATCH /books/1 {"title": null}` → **`500`**.
`BookPatch` `null`'u kabul ediyor (`str | None`), kayıt `title: None` oluyor,
sonra yanıt modeli `BookOut` (`title: str`) bunu reddediyor. Kayıt da bozuk
kaldı. Çözüm: `PATCH`'te gönderilen `null`'u baştan reddetmek:

```python
class BookPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    year: int | None = None

    @field_validator("title", "year")
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("may not be null")
        return value
```

Doğrulayıcı yalnızca **gönderilen** alanlarda çalışıyor (varsayılan
`None` denetlenmiyor). Artık `{"title": null}` → `422`, `{}` ve
`{"year": 1966}` → `200`.

## Silmek

```python
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    find_book(book_id)
    del books[book_id]
```

## Bütün akış (ölçüldü)

```text
POST   /books      {"title": "Dune", "year": 1965}  201 {"title":"Dune","year":1965,"id":1}
POST   /books      Emma, Ubik                       201 id 2, 3
GET    /books?year=1815                             200 [{"title":"Emma",...,"id":2}]
GET    /books/9                                     404 {"detail":"Book not found"}
PATCH  /books/1    {"year": 1966}                   200 {"title":"Dune","year":1966,"id":1}
DELETE /books/3                                     204
DELETE /books/3                                     404
POST   /books      {"title": "Kindred", ...}        201 ... "id":4
```

Son satır önemli: 3 silindi ama yeni kitap `4` aldı; numara hiç tekrar
etmiyor. Cevaptaki alan sırası `title, year, id`, çünkü `BookOut`
`BookIn`'den türedi ve önce taban modelin alanları geliyor.

## Özet

- İki adres (`/books`, `/books/{id}`) + beş yöntem = CRUD.
- Kimlik için geri gitmeyen sayaç; `len() + 1` silmeden sonra kayıt ezer.
- Ortak "bul ya da 404" yardımcısı.
- `PUT` tamamını (`BookIn`), `PATCH` gönderileni (`BookPatch` +
  `exclude_unset=True`) değiştirir.
- Oluşturma `201`, silme `204`, bulunamayan `404`.
