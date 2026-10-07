Aynı başlıkları her istekte tekrar yazmak yerine bir oturum kur.

**Yapman gerekenler:**

1. `session = requests.Session()` ile bir oturum aç ve `session.headers`'a
   üç başlık ekle:
   - `Authorization: Bearer letmein`
   - `X-API-Key: demo-key-123`
   - `User-Agent: library-cli/1.0`
2. Oturumla üç istek gönder: `/me`, `/stats`, `/books/2`. Her birinin
   adresini ve durum kodunu yazdır.
3. Son satırda üçüncü isteğin giden `User-Agent` başlığını
   (`r.request.headers`) yazdır.

**Beklenen çıktı:**

```
/me 200
/stats 200
/books/2 200
user agent: library-cli/1.0
```
