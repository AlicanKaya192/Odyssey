Bir uç noktayı REST'in "adreste fiil olmaz" kuralıyla denetleyen bir fonksiyon
yaz. Burada istek yok.

**Yapman gerekenler:** `check_endpoint(method, path)` fonksiyonunu yaz:

1. Yolu `/` ile parçalara böl (boş parçaları at). Parçalardan biri küçük
   harfe çevrildiğinde `get`, `create`, `update`, `delete`, `remove`, `add`
   kelimelerinden biriyle **başlıyorsa** `"verb in path"` döndür.
2. Yoksa `"ok"` döndür.

Kısacası: **adreste fiil varsa** `"verb in path"`, yoksa `"ok"`. Sonra
`endpoints` listesindeki her uç nokta için sonucu yazdır.

**Beklenen çıktı:**

```
GET /books -> ok
GET /getBooks -> verb in path
POST /books/42/delete -> verb in path
DELETE /books/42 -> ok
POST /createBook -> verb in path
GET /authors/6/books -> ok
PATCH /books/42 -> ok
```
