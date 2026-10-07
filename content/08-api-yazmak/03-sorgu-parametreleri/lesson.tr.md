# Sorgu Parametreleri

API 1'de bir listeyi süzmek ve sayfalamak için adresin sonuna `?` ile
eklenen **sorgu parametrelerini** kullanmıştın: `/books?page=2`,
`/books?author=Austen`. `requests`'te bunlar `params=` ile gidiyordu. Şimdi
onları karşılayan tarafı yazıyorsun.

## Yolda olmayan her parametre bir sorgudur

```python
@app.get("/books")
def list_books(page: int = 1):
    return {"page": page}
```

Adreste `{page}` yok; FastAPI bu yüzden `page`'i **sorgu parametresi**
sayıyor ve değeri `?page=...` kısmından alıyor:

```text
GET /books           {"page": 1}    (gönderilmedi → varsayılan)
GET /books?page=3    {"page": 3}
GET /books?page=x    422            (loc: ["query", "page"])
```

Kural basit:

| İşlevde | FastAPI'nin anladığı |
|---|---|
| Adreste `{ad}` var | Yol parametresi |
| Adreste yok | Sorgu parametresi |

Tip çevirme ve `422` yol parametresindekiyle aynı; tek fark `loc`'un ilk
öğesi: `path` yerine `query`.

## Zorunlu mu, isteğe bağlı mı?

Varsayılan değer **verirsen** parametre isteğe bağlı olur, **vermezsen**
zorunlu:

```python
@app.get("/search")
def search(q: str):          # varsayılan yok → zorunlu
    return {"q": q}
```

```text
GET /search          422  type: missing, loc: ["query", "q"], msg: Field required
GET /search?q=dune   200  {"q": "dune"}
```

## "Yoksa hiç süzme": `None`

Bazen bir süzgeç ya verilir ya verilmez; verilmezse hiçbir şey süzülmez.
Bunun için varsayılan `None` ve tip `int | None`:

```python
@app.get("/books")
def list_books(year_from: int | None = None):
    if year_from is None:
        return books
    return [book for book in books if book["year"] >= year_from]
```

`int | None` "ya tam sayı ya hiçbir şey" demek. `?year_from=1950` gelirse
`1950`, gelmezse `None`.

## Sayfalama

API 1'de bir API'den sayfa sayfa veri çekmiştin. Sayfalayan taraf şöyle
yazılıyor:

```python
@app.get("/books")
def list_books(page: int = 1, per_page: int = 2):
    start = (page - 1) * per_page
    return {"page": page, "total": len(books), "items": books[start:start + per_page]}
```

<figure class="fig">
  <div class="flow">
    <span class="node ok">Sayfa 1<br><small>[0:2] Dune, Emma</small></span>
    <span class="node">Sayfa 2<br><small>[2:4] Ulysses, Kindred</small></span>
    <span class="node">Sayfa 3<br><small>[4:6] Beloved</small></span>
  </div>
  <figcaption><code>per_page=2</code> ile beş kitap üç sayfaya bölünüyor. Sayfa <code>p</code> için dilimin başı <code>(p - 1) * per_page</code>; son sayfa eksik olabilir.</figcaption>
</figure>

Beş kitapla ölçtük:

```text
GET /books                      page 1: Dune, Emma
GET /books?page=2               page 2: Ulysses, Kindred
GET /books?page=3&per_page=2    page 3: Beloved
```

`total` istemciye kaç sayfa olduğunu hesaplatıyor; API 1'de son sayfayı
anlamak için tam olarak buna bakıyordun.

## Diğer tipler

```python
@app.get("/flag")
def flag(available: bool = False):
    return available
```

`?available=true` (ya da `1`, `yes`, `on`) → `true`; gönderilmezse `false`.

Aynı adın birden çok kez gönderildiği liste (`?tag=a&tag=b`) için
`Query` gerekiyor:

```python
from fastapi import FastAPI, Query


@app.get("/tags")
def tags(tag: list[str] = Query(default=[])):
    return tag
```

`GET /tags?tag=a&tag=b` → `["a", "b"]`. `Query` olmadan FastAPI listeyi
gövde sanıyor.

## Bilinmeyen parametre

`GET /books?unknown=1` hata vermiyor: FastAPI tanımadığı sorgu
parametrelerini **yok sayıyor** (ölçtük). Bir yazım hatası (`?pgae=2`)
sessizce varsayılana düşer; istemci "neden hep ilk sayfa?" diye şaşırabilir.
Belgen (`/docs`) bu yüzden önemli: hangi parametrelerin var olduğunu orada
görüyorlar.

## Yol ve sorgu birlikte

```python
@app.get("/authors/{author}/books")
def author_books(author: str, year_from: int | None = None):
    ...
```

`GET /authors/Austen/books?year_from=1810`: `author` yoldan, `year_from`
sorgudan. Hangisinin nereden geldiğini adres belirliyor.

## Özet

- Adreste olmayan parametre sorgudan okunur (`?ad=değer`).
- Varsayılan yoksa zorunlu (`422 missing`), varsa isteğe bağlı.
- "Verilmezse süzme" için `int | None = None`.
- Sayfalama: `start = (page - 1) * per_page`, dilim `[start:start + per_page]`,
  yanında `total`.
- Liste için `Query(default=[])`; bilinmeyen parametreler yok sayılır.
