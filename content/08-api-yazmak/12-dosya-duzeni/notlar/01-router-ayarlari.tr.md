`APIRouter` ve `include_router`'ın en sık kullanılan ayarları.

## `APIRouter(...)`

| Ayar | Ne yapar? |
|---|---|
| `prefix="/books"` | Bütün adreslerin başına eklenir |
| `tags=["books"]` | `/docs`'ta başlık |
| `dependencies=[Depends(f)]` | Router'daki her uç noktada çalışır |

## `app.include_router(router, ...)`

Aynı ayarlar burada da verilebilir ve router'dakilerin **üstüne** eklenir.
En yaygın kullanım sürüm öneki:

```python
app.include_router(books.router, prefix="/v1")
```

Ölçtük: router'ın kendi öneki `/books` iken adres `/v1/books` oldu,
`/books` artık `404`.

## Sürüm öneki neden?

API'yi kullanan uygulamalar var ve bir gün cevabın biçimini değiştirmen
gerekiyor. Eski istemcileri bozmamak için yeni biçimi `/v2/books`'ta
açarsın, `/v1/books` bir süre eskisi gibi çalışır.

```python
app.include_router(books_v1.router, prefix="/v1")
app.include_router(books_v2.router, prefix="/v2")
```

## Router içinde router

Bir router başka bir router'ı da içerebilir:
`router.include_router(reviews.router)`. Büyük projelerde
`/books/{id}/reviews` gibi alt kaynaklar böyle ayrılır.

## Adres yazımı

| Router öneki | Uç nokta | Gerçek adres |
|---|---|---|
| `/books` | `""` | `/books` |
| `/books` | `"/{book_id}"` | `/books/{book_id}` |
| `/books` | `"/"` | `/books/` (sonda eğik çizgi) |

İkinci ve üçüncüsünü karıştırma: `"/"` yazarsan liste adresi `/books/`
olur, `/books` isteği yönlendirilir.
