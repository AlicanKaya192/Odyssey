Her HTTP isteğinin ilk satırı üç parçadan oluşuyor: yöntem, hedef ve sürüm.
Aralarında birer boşluk var.

**Yapman gerekenler:**

1. `parse_request_line(line)` fonksiyonunu yaz. Şu sözlüğü döndürsün:
   `{"method": ..., "target": ..., "version": ...}`.
2. `lines` listesindeki her satır için yöntemi ve hedefi aşağıdaki biçimde
   yazdır.

**Beklenen çıktı:**

```
GET -> /v1/books?author=Austen
POST -> /v1/books
DELETE -> /v1/books/42
```
