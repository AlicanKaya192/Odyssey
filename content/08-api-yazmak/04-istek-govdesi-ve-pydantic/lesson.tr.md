# İstek Gövdesi ve Pydantic

Şimdiye kadar bütün bilgi adresle geldi: yol ve sorgu. Yeni bir kitap
eklerken ise başlık, yıl, etiketler, not... adrese sığmaz ve sığmamalı.
API 1'de `requests.post(url, json={...})` ile bir **gövde** göndermiştin.
Bu bölümde gövdeyi karşılayan tarafı yazıyorsun; gövdenin şeklini de
**Pydantic** ile tarif ediyorsun.

## Gövdenin kalıbı: model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    year: int
```

`Book` bir **model**: gelen JSON'un hangi alanları, hangi tiplerde içermesi
gerektiğini söyleyen kalıp. Python patikasında sınıf yazmıştın; burada
yalnızca alanları ve tiplerini sıralıyorsun, gerisini `BaseModel`
yapıyor.

Uç noktada parametrenin tipi bu model olunca FastAPI değeri **gövdeden**
okuyor:

```python
books = []


@app.post("/books", status_code=201)
def add_book(book: Book):
    books.append(book)
    return {"id": len(books), **book.model_dump()}
```

- `book: Book`: gövde `Book` kalıbına uymalı.
- `book.title`, `book.year`: alanlara nokta ile ulaşılıyor.
- `book.model_dump()`: modeli sözlüğe çeviriyor; `**` ile başka bir
  sözlüğün içine açılıyor.
- `status_code=201`: "oluşturuldu" kodu. Ayrıntısı Yanıt Modelleri ve Durum
  Kodları bölümünde.

<figure class="fig">
  <div class="flow">
    <span class="node">Gövde (JSON)<br><small>{"title": "Dune", "year": "1965"}</small></span><span class="arrow">→</span>
    <span class="node acc">Book modeli<br><small>title: str, year: int</small></span><span class="arrow">→</span>
    <span class="node ok">book nesnesi<br><small>book.year == 1965</small></span>
  </div>
  <figcaption>Gövde önce modelin kalıbından geçiyor: alanlar denetleniyor ve çevrilebilenler çevriliyor. Uymazsa işlev hiç çağrılmıyor, <code>422</code> gidiyor.</figcaption>
</figure>

## Denetim kendiliğinden

Gövde kalıba uymazsa işlev çağrılmıyor; FastAPI `422` veriyor. Ölçtüklerimiz:

| Gönderilen gövde | Sonuç |
|---|---|
| `{"title": "Dune", "year": 1965}` | `201` |
| `{"title": "Dune"}` | `422` missing, `loc: ["body", "year"]` |
| `{"title": "Dune", "year": "nineteen"}` | `422` int_parsing |
| `{"title": 5, "year": 1965}` | `422` string_type |
| `{"title": "Dune", "year": 1965.5}` | `422` int_from_float |
| `{"title": "Dune", "year": "1965"}` | `201`: metin sayıya çevrildi |

İki şey dikkat çekiyor:

- `"1965"` (tırnaklı) kabul edildi: Pydantic sayıya çevrilebilen metni
  çeviriyor. Ama `5`'i metne çevirmiyor ve `1965.5`'i tam sayı yapmıyor;
  bilgi kaybedecek çevirmeleri reddediyor.
- `loc` artık `body` ile başlıyor: hatanın gövdenin hangi alanında olduğunu
  söylüyor.

Gövde hiç yoksa ya da JSON bozuksa da `422`:

```text
(gövde yok)      422  type: missing, loc: ["body"]
{bad json        422  type: json_invalid, msg: JSON decode error
```

## İsteğe bağlı alanlar

Varsayılan değer verilen alan isteğe bağlı olur:

```python
class Book(BaseModel):
    title: str
    year: int
    tags: list[str] = []
    note: str | None = None
```

`{"title": "Dune", "year": 1965}` gönderilince `tags` `[]`, `note`
`null` oluyor. Sorgu parametrelerindeki kuralın aynısı: varsayılan yoksa
zorunlu.

## Fazladan alanlar sessizce atılır

`{"title": "Dune", "year": 1965, "extra": 1}` → `201`, ama `extra` modelde
yok ve **atılıyor** (ölçtük). Bu bir güvenlik özelliği de: istemci
`{"is_admin": true}` gönderse bile modelinde öyle bir alan yoksa koduna
ulaşmaz. Sakıncası: yanlış yazılmış bir alan (`"yaer"`) hata vermeden
kaybolur; eksik `year` yüzünden `422` alırsın ve sebebi oradan anlarsın.

## İç içe modeller

Bir model başka bir modeli alan olarak içerebilir:

```python
class Author(BaseModel):
    name: str


class BookWithAuthor(BaseModel):
    title: str
    author: Author
```

`{"title": "Emma", "author": {"name": "Austen"}}` gönderilince
`item.author` bir `Author` nesnesi, `item.author.name` `"Austen"`. Liste de
olur: `items: list[Item]`.

## Model döndürmek

İşlev modeli doğrudan döndürebilir; FastAPI onu JSON'a çevirir:

```python
@app.post("/echo")
def echo(book: Book):
    return book
```

```text
POST /echo  {"title": "Dune", "year": 1965, "tags": ["sf"]}
200         {"title":"Dune","year":1965,"tags":["sf"],"note":null}
```

## Yol + gövde birlikte

Bir kaydı güncellerken hangi kayıt yoldan, yeni değerler gövdeden gelir:

```python
@app.put("/books/{book_id}")
def replace_book(book_id: int, book: Book):
    ...
```

FastAPI üç kaynağı parametrenin şeklinden ayırıyor:

| Parametre | Nereden? |
|---|---|
| Adreste `{book_id}` var | Yol |
| Basit tip (`int`, `str`...), adreste yok | Sorgu |
| Pydantic modeli | Gövde |

## `/docs`'ta

`POST /books` açıldığında Swagger UI gövde için hazır bir örnek gösteriyor
(`{"title": "string", "year": 0, ...}`) ve aşağıda `Book` şemasını
listeliyor: alanlar, tipler, hangisinin zorunlu olduğu. Bunların hepsi
modelden geldi.

## Özet

- Gövdenin kalıbı bir Pydantic modeli: `class Book(BaseModel)` + tipli
  alanlar.
- Model tipli parametre gövdeden okunur; `book.title`, `book.model_dump()`.
- Uymayan gövde `422` (`loc: ["body", ...]`); bilgi kaybetmeyen çevirmeler
  (`"1965"` → `1965`) yapılır.
- Varsayılanlı alan isteğe bağlı; fazladan alanlar atılır.
- Yol + sorgu + gövde aynı uç noktada birlikte kullanılabilir.
