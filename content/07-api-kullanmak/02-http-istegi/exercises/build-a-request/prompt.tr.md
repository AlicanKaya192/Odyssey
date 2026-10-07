Bir istek kütüphanesinin yaptığı işi küçük bir fonksiyonla sen yapacaksın:
isteğin metnini kurmak.

**Yapman gerekenler:** `build_request(method, target, host, body="")`
fonksiyonunu yaz. Döndürdüğü metin satırlardan oluşsun, satırlar `"\n"`
ile birleşsin:

1. İstek satırı: `<method> <target> HTTP/1.1`
2. `Host: <host>`
3. `body` boş değilse iki başlık daha:
   `Content-Type: application/json` ve `Content-Length: <bayt sayısı>`.
   Bayt sayısı `len(body.encode("utf-8"))`.
4. Başlıklardan sonra bir boş satır, ardından `body`.

Yani metin, başlık satırlarının `"\n"` ile birleşimi + `"\n\n"` + `body`.

Sonra aşağıdaki iki isteği yazdır, araya `---` koy.

**Beklenen çıktı:**

```
GET /v1/books?author=Austen HTTP/1.1
Host: api.example.com


---
POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 17

{"title": "Emma"}
```

`GET` isteğinde gövde yok; metin boş satırla bitiyor.
