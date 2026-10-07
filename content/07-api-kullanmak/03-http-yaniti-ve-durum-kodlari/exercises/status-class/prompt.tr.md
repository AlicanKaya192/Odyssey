Durum kodunun ilk hanesi sınıfını söylüyor. Bunu bir fonksiyona dönüştür.

**Yapman gerekenler:**

1. `status_class(code)` fonksiyonunu yaz. İlk haneye (`code // 100`) göre
   şunlardan birini döndürsün: `"info"` (1), `"success"` (2), `"redirect"`
   (3), `"client error"` (4), `"server error"` (5).
2. `codes` listesindeki her kod için kodu ve sınıfını yazdır.

**Beklenen çıktı:**

```
200 success
201 success
304 redirect
404 client error
429 client error
500 server error
503 server error
```
