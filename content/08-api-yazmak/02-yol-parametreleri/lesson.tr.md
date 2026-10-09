# Yol Parametreleri

Bir kitap API'sinde her kitabın kendi adresi olur: `/books/1`, `/books/2`,
`/books/42`. Her kitap için ayrı bir işlev yazmak imkânsız. Bunun yerine
adresin değişen kısmını bir **yol parametresi** olarak tanımlarsın: tek
işlev, sonsuz adres.

## Süslü parantezle yer ayırmak

```python
books = {1: {"id": 1, "title": "Dune"}, 2: {"id": 2, "title": "Emma"}}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return books[book_id]
```

- `{book_id}` adresin o parçasını bir **değişkene** ayırıyor.
- İşlevin parametresi **aynı adla** (`book_id`) yazılıyor; FastAPI adresteki
  değeri oraya koyuyor.
- `: int` FastAPI'ye "bu bir tam sayı olmalı" diyor.

<figure class="fig">
  <div class="anat">
    <div class="sig"><code>GET /books/<b>2</b></code> → <code>@app.get("/books/<b>{book_id}</b>")</code> → <code>get_book(<b>book_id</b>: int)</code></div>
    <div class="legend">
      <div><b>2</b> adresten gelen metin: <code>"2"</code></div>
      <div><b>{book_id}</b> adresin bu parçası bir değişken</div>
      <div><b>book_id: int</b> aynı ad; FastAPI <code>"2"</code>'yi <code>2</code>'ye çeviriyor</div>
    </div>
  </div>
  <figcaption>Adresteki parça, süslü parantezdeki ad ve işlevin parametresi aynı adla birbirine bağlanıyor.</figcaption>
</figure>

## Tip: çevirme ve denetleme

Adres her zaman metindir: `/books/2` gelince elde `"2"` var. `book_id: int`
yazdığın için FastAPI onu **sayıya çeviriyor**; işlevin içinde `book_id`
`2` (tam sayı) oluyor ve sözlükte `books[2]` diye arayabiliyorsun.

Çevrilemezse işlevin hiç çağrılmadan isteği reddediyor (ölçtük):

```text
GET /books/2      200  {"book_id": 2, "type": "int"}
GET /books/abc    422
GET /books/2.5    422
```

`422`'nin gövdesi neyin yanlış olduğunu söylüyor:

```json
{"detail": [{
  "type": "int_parsing",
  "loc": ["path", "book_id"],
  "msg": "Input should be a valid integer, unable to parse string as an integer",
  "input": "abc"}]}
```

| Alan | Anlamı |
|---|---|
| `loc` | Nerede: `path` içindeki `book_id` |
| `msg` | Ne bekleniyordu |
| `input` | Ne geldi |

API Kullanmak modülünde bir API'den `422` aldığında okuduğun gövde tam olarak buydu.
Şimdi sen yazmadın, FastAPI tip belirtiminden üretti.

Tip yazmazsan (`def get_book(book_id):`) değer metin kalır ve
`books["2"]` bulunamaz; tipi her zaman yaz.

## Bulunamayan kayıt: 404

`/books/99` geçerli bir sayı ama böyle bir kitap yok. `books[99]` bir
`KeyError` atar ve istemci `500` alır: sunucu hatası gibi görünür, oysa
hata istemcinin istediği kayıtta. Doğrusu `404`:

```python
from fastapi import FastAPI, HTTPException


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
```

`raise HTTPException(...)` işlevi o an durdurup istemciye verilen kod ve
`{"detail": "Book not found"}` gövdesiyle cevap veriyor. Ayrıntısını Hata
Yanıtları bölümünde göreceğiz; şimdilik kalıbı bilmen yeter.

## Metin parametreleri ve boşluk

```python
@app.get("/hello/{name}")
def hello(name: str):
    return {"greeting": "Hello, " + name}
```

`GET /hello/Ada` → `{"greeting": "Hello, Ada"}`. Adreste boşluk `%20`
olarak gelir (`/hello/Ada%20Lovelace`); FastAPI onu çözüp `"Ada Lovelace"`
yapıyor.

## Birden çok parametre

```python
@app.get("/users/{user_id}/books/{book_id}")
def user_book(user_id: int, book_id: int):
    return {"user": user_id, "book": book_id}
```

`GET /users/7/books/3` → `{"user": 7, "book": 3}`. Her süslü parantez için
aynı adlı bir parametre.

## Sıralama tuzağı

İki uç nokta düşün: bir kitabı kimliğiyle getiren `/books/{book_id}` ve en
son kitabı getiren `/books/latest`. Bu sırayla yazarsan:

```python
@app.get("/books/{book_id}")
def get_book(book_id: int): ...


@app.get("/books/latest")
def latest(): ...
```

`GET /books/latest` **ilk** eşleşen yola gidiyor: `{book_id}` her şeyi
yakalıyor, `"latest"` sayıya çevrilemiyor ve `422` dönüyor (ölçtük).
`latest` hiç çağrılmıyor.

Kural: **sabit yolları değişkenli yollardan önce yaz.**

```python
@app.get("/books/latest")
def latest(): ...


@app.get("/books/{book_id}")
def get_book(book_id: int): ...
```

## Belgede

`/docs` sayfasında `book_id` "path" parametresi, tipi `integer` ve zorunlu
olarak görünüyor; "Try it out" bir kutu açıp değeri soruyor. Bunu da tip
belirtiminden çıkardı.

## Özet

- `"/books/{book_id}"` + `def f(book_id: int)`: adın ikisinde de aynı olması
  şart.
- Tip belirtimi değeri çeviriyor ve denetliyor; uymazsa `422` ve hatanın
  yerini söyleyen gövde.
- Olmayan kayıt için `raise HTTPException(status_code=404, detail=...)`;
  yoksa `500`.
- Sabit yollar (`/books/latest`) değişkenli yollardan (`/books/{book_id}`)
  önce.
