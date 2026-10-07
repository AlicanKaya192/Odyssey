# Doğrulama

Önceki bölümde Pydantic gövdenin **tipini** denetledi: `year` tam sayı mı,
`title` metin mi. Ama tip doğru olsa da değer saçma olabilir: `year`
`-500`, `title` boş metin, sayfa boyu `10000`. Bu bölümde değerin
**kendisine** kural koyuyorsun; kurala uymayan istek işlevine hiç ulaşmıyor.

## Neden sunucu denetler?

İstemci (tarayıcı, mobil uygulama) da denetim yapabilir, ama ona
güvenemezsin: herkes `requests` ile ya da `curl` ile istediği gövdeyi
gönderebilir. Veriyi saklayan ve kullanan sunucu olduğu için **son söz
sunucunun**. FastAPI'de bunu `if` yığınlarıyla değil, alanın yanına
yazılan kurallarla yaparsın.

## `Field`: alanın kuralları

```python
from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1450, le=2100)
    rating: float = Field(default=0, ge=0, le=5)
    isbn: str | None = Field(default=None, pattern=r"^[0-9]{13}$")
```

- Sayılar için `gt` (büyük), `ge` (büyük ya da eşit), `lt` (küçük), `le`
  (küçük ya da eşit). Adları İngilizce kısaltmalardan: **g**reater **t**han,
  **g**reater or **e**qual...
- Metinler için `min_length`, `max_length` ve `pattern` (düzenli ifade).
- `default=` verilirse alan isteğe bağlı olur, tıpkı `= 0` yazmak gibi.

`pattern=r"^[0-9]{13}$"`: baştan (`^`) sona (`$`) tam 13 rakam. Düzenli
ifadeyi ayrıntılı bilmen gerekmiyor; en sık kullanılanlar notta.

<figure class="fig">
  <div class="flow">
    <span class="node">Gövde<br><small>JSON</small></span><span class="arrow">→</span>
    <span class="node">Tip<br><small>year: int</small></span><span class="arrow">→</span>
    <span class="node acc">Kural<br><small>Field(ge=1450)</small></span><span class="arrow">→</span>
    <span class="node acc">Doğrulayıcı<br><small>field_validator</small></span><span class="arrow">→</span>
    <span class="node ok">İşlevin</span>
  </div>
  <figcaption>İstek sırayla üç denetimden geçiyor. Herhangi birinde takılırsa işlevin hiç çağrılmıyor ve <code>422</code> gidiyor.</figcaption>
</figure>

## Ölçtüklerimiz

| Gönderilen | Sonuç |
|---|---|
| `{"title": "Dune", "year": 1965}` | `200`, `rating` `0.0`, `isbn` `null` |
| `{"title": "", "year": 1965}` | `422` string_too_short |
| `{"title": "Dune", "year": 3000}` | `422` less_than_equal |
| `{"title": "Dune", "year": 1965, "rating": 7}` | `422` less_than_equal |
| `{"title": "Dune", "year": 1965, "isbn": "123"}` | `422` string_pattern_mismatch |

Hata gövdesi kuralı da söylüyor:

```json
{"type": "less_than_equal", "loc": ["body", "year"],
 "msg": "Input should be less than or equal to 2100",
 "input": 3000, "ctx": {"le": 2100}}
```

Birden fazla alan bozuksa **hepsi** tek cevapta geliyor:
`{"title": "", "year": 3000}` iki hatalı `detail` listesi döndürdü. İstemci
bütün hataları bir kerede düzeltebiliyor.

## Yol ve sorguda kurallar

Sorgu ve yol parametrelerine de aynı kurallar konur. Bunun için tipin
yanına `Query` ya da `Path` yazılır; ikisi `Annotated` içinde:

```python
from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/books")
def list_books(limit: Annotated[int, Query(ge=1, le=50)] = 10):
    return {"limit": limit}


@app.get("/books/{book_id}")
def get_book(book_id: Annotated[int, Path(gt=0)]):
    return {"id": book_id}
```

`Annotated[int, Query(ge=1, le=50)]` şu demek: "tipi `int`, ek bilgisi
`Query(...)`". Varsayılan değer yine `= 10` ile en sonda.

```text
GET /books?limit=100   422  less_than_equal, loc ["query", "limit"]
GET /books?limit=0     422  greater_than_equal
GET /books             200  {"limit": 10}
GET /books/0           422  greater_than, loc ["path", "book_id"]
```

`loc`'un ilk öğesi hatanın nerede olduğunu söylüyor: `body`, `query` ya da
`path`.

## Yalnızca belli değerler: `Literal`

Bir alan yalnızca birkaç değerden birini alabiliyorsa:

```python
from typing import Literal


class Order(BaseModel):
    size: Literal["small", "medium", "large"]
```

`{"size": "huge"}` → `422` literal_error, mesaj seçenekleri sayıyor:
`Input should be 'small', 'medium' or 'large'`. `/docs` sayfası da bu
alanı açılır liste olarak gösteriyor.

## Kendi kuralın: `field_validator`

Hazır kurallar yetmezse kendi denetimini yazarsın:

```python
from pydantic import BaseModel, field_validator


class User(BaseModel):
    name: str
    username: str

    @field_validator("username")
    @classmethod
    def no_spaces(cls, value: str) -> str:
        if " " in value:
            raise ValueError("must not contain spaces")
        return value.lower()
```

- İşlev alanın değerini alıyor (tip denetiminden **sonra**, yani `value`
  burada kesin bir metin).
- Kural bozuksa `ValueError` fırlatıyorsun; Pydantic onu `422`'ye çeviriyor.
- Döndürdüğün değer alanın yeni değeri oluyor: burada küçük harfe
  çevrildi.

```text
{"username": "ada lovelace"}  422  value_error, "Value error, must not contain spaces"
{"username": "AdaL"}          200  {"name": "Ada", "username": "adal"}
```

`@classmethod` satırı Pydantic belgelerindeki kalıp. Yazılmasa da çalışıyor
(ölçtük), ama ilk parametrenin nesne değil sınıf olduğunu okuyana o
söylüyor; yaz.

## İki alanı birlikte denetlemek: `model_validator`

"Bitiş, başlangıçtan önce olamaz" gibi bir kural tek bir alana ait değil.
Bütün model dolduktan sonra çalışan denetim:

```python
from pydantic import BaseModel, model_validator


class Trip(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_order(self):
        if self.end < self.start:
            raise ValueError("end must not be before start")
        return self
```

`mode="after"`: alanlar denetlendikten sonra; işlev `self` alıyor ve
**`self`'i döndürmeli**. Hatanın `loc`'u alan değil, gövdenin kendisi:
`["body"]`.

## Boşluk tuzağı

`Field(min_length=1)` olan bir ada `"  "` (iki boşluk) gönderdik: **`200`**.
İki boşluk da iki karakter. Kenar boşluklarını önce atmak için modele:

```python
from pydantic import BaseModel, ConfigDict, Field


class Author(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1)
```

Artık `"  "` → `422`, `"  Ada "` → `"Ada"`.

## Özet

- Değerin kuralları alanın yanında: `Field(ge=..., le=..., min_length=...,
  max_length=..., pattern=...)`.
- Sorgu ve yolda `Annotated[int, Query(...)]`, `Annotated[int, Path(...)]`.
- Seçeneklerden biri: `Literal[...]`.
- Kendi kuralın: `@field_validator` (bir alan), `@model_validator(mode="after")`
  (alanlar birlikte); hata `ValueError`, sonuç `422`.
- Bütün hatalar tek cevapta gelir; `loc` nerede, `type` ne olduğunu söyler.
