API Kullanmak modülünde REST'i okurken gördüğün adres kurallarını, bu sefer adresi
yazan olarak.

## Kaynak ve kimlik

| Adres | Anlamı |
|---|---|
| `/books` | Kitapların hepsi (topluluk) |
| `/books/42` | Kimliği 42 olan kitap |
| `/authors/7/books` | 7 numaralı yazarın kitapları |
| `/authors/7/books/3` | O yazarın 3 numaralı kitabı |

- Çoğul ad, küçük harf, kelimeler arası tire: `/book-reviews`.
- İç içe yol en fazla iki düzey; daha derini okunmaz olur. Gerekirse sorgu
  parametresi: `/books?author_id=7` (Sorgu Parametreleri bölümü).
- Kimlik genellikle sayı (`/books/42`); okunur ad (`/books/dune`) da
  olabilir, ama ad değişince adres değişir.

## Fiil değil ad

| Yerine | Yaz |
|---|---|
| `GET /getBook/42` | `GET /books/42` |
| `POST /books/42/delete` | `DELETE /books/42` |
| `GET /books/create?title=Dune` | `POST /books` (gövdeyle) |

## Sıralama

Uç noktalar **yazıldığı sırayla** denenir, ilk eşleşen kazanır. Sabit
parçalı yollar önce:

```python
@app.get("/books/latest")       # 1. sabit
@app.get("/books/{book_id}")    # 2. değişkenli
```

Aynı yere iki değişkenli yol da yazılmaz: `/books/{book_id}` ile
`/books/{title}` aynı adresleri yakalar; ikincisi hiç çalışmaz.

## Akılda kalsın

> Adres bir şeyin adıdır; yapılacak işi yöntem söyler. Adresteki her süslü
> parantez, işlevde aynı adlı ve tipli bir parametredir.
