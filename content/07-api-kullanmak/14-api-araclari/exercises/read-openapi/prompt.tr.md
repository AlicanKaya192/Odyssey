Alıştırma sunucusu kendini `GET /openapi.json` ile anlatıyor. Swagger UI'ın
yaptığı ilk işi sen yap: belgeyi oku ve uç noktaları listele.

**Yapman gerekenler:**

1. Belgeyi iste; API'nin adını ve sürümünü (`info`) yazdır.
2. `paths` içindeki her yol ve her yöntem için `YÖNTEM yol - özet` satırı
   kur; kimlik isteyenlerin (`security` alanı olanlar) sonuna ` (auth)`
   ekle. Satırları `endpoints` listesinde topla ve yazdır.
3. Kimlik isteyen işlem sayısını yazdır.

**Beklenen çıktı:**

```
Odyssey Library API 1.0
GET /books - List books
POST /books - Add a book (auth)
GET /books/{id} - Get one book
PUT /books/{id} - Replace a book (auth)
PATCH /books/{id} - Change a book (auth)
DELETE /books/{id} - Delete a book (auth)
GET /authors - List authors
GET /authors/{id}/books - Books of one author
GET /stats - Library statistics (auth)
need auth: 5
```
