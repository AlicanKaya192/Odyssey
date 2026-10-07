Kütüphane API'si için küçük bir istemci sınıfı yaz. Her metot REST sözleşmesine
göre bir istek gönderecek.

**Yapman gerekenler:** `LibraryClient` sınıfını yaz:

- `__init__(self, base, token)`: bir `requests.Session` kursun ve
  `Authorization: Bearer <token>` başlığını eklesin.
- `create(self, book)`: `POST /books`; yeni kitabın **kimliğini** döndürsün.
- `change(self, book_id, fields)`: `PATCH /books/<id>`; güncel kitabı
  (sözlük) döndürsün.
- `read(self, book_id)`: `GET /books/<id>`; kitabı döndürsün, yoksa `None`.
- `remove(self, book_id)`: `DELETE /books/<id>`; durum kodunu döndürsün.

Sonra istemciyle bir kitap oluştur, fiyatını değiştir, oku, sil ve yeniden
oku; her adımı aşağıdaki gibi yazdır.

**Beklenen çıktı:**

```
created: 24
changed price: 9.0
read: Kindred 9.0
remove: 204
read after remove: None
```
