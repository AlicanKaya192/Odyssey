Bölüm 08 ve 09'un tekrarı: kimlikle yazmak ve sonucu doğrulamak.

**Yapman gerekenler:**

1. Jetonu `os.environ.get("LIBRARY_TOKEN", "letmein")` ile al, bir oturuma
   `Authorization` başlığı olarak ekle.
2. `{"title": "The Word for World Is Forest", "price": 11.5, "author_id": 6}` kitabını ekle;
   kodu ve `Location`'ı yazdır.
3. `Location`'daki adrese `PATCH` ile fiyatı `9.99` yap.
4. Aynı adresi `GET` ile okuyup başlığı, yazarı ve fiyatı yazdır.

**Beklenen çıktı:**

```
created: 201 /books/24
patched: 200
The Word for World Is Forest Le Guin 9.99
```
