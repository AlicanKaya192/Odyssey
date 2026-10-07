Sorgu parametresi yazmanın bütün kalıpları tek tabloda.

| İstek | İşlevde | Gönderilmezse |
|---|---|---|
| `?q=dune` (zorunlu) | `q: str` | `422 missing` |
| `?page=2` | `page: int = 1` | `1` |
| <code>?year_from=1950</code> (süzgeç) | <code>year_from: int &#124; None = None</code> | <code>None</code> → süzme |
| `?available=true` | `available: bool = False` | `false` |
| `?tag=a&tag=b` | `tag: list[str] = Query(default=[])` | `[]` |
| <code>/authors/Austen/books?year_from=1810</code> | <code>author: str, year_from: int &#124; None = None</code> | — |

## Süzgeç kalıbı

```python
@app.get("/books")
def list_books(author: str | None = None, year_from: int | None = None):
    found = books
    if author is not None:
        found = [b for b in found if b["author"] == author]
    if year_from is not None:
        found = [b for b in found if b["year"] >= year_from]
    return found
```

Her süzgeç bir öncekinin sonucunu daraltıyor; verilmeyen atlanıyor.

## Sayfalama kalıbı

```python
@app.get("/books")
def list_books(page: int = 1, per_page: int = 10):
    start = (page - 1) * per_page
    items = books[start:start + per_page]
    return {"page": page, "per_page": per_page, "total": len(books), "items": items}
```

- Sayfa 1'den başlar (insanlar böyle sayar); dilim için 1 çıkarılıyor.
- Listenin sonunu aşan sayfa hata değil, boş `items`.
- `total` olmadan istemci son sayfayı ancak boş sayfa gelince anlar.
- Önce süz, sonra say ve dilimle: `total` süzülmüş listenin uzunluğu.

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Hep varsayılan değer geliyor | İstemci adı farklı yazıyor (`?pgae=2`); bilinmeyen yok sayılıyor |
| `422 missing` beklenmedik yerde | Varsayılan unutulmuş, parametre zorunlu olmuş |
| Liste parametresi gövde isteniyor | `Query(default=[])` yazılmamış |
| Süzgeç hiç işlemiyor | `if year_from:` yazılmış; `0` da "yok" sayıldı → `is not None` |
