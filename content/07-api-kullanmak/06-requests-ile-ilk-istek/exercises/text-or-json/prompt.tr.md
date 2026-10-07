Her uç nokta JSON döndürmüyor: `/status` düz metin. Gövdeyi türüne göre
okuyan bir fonksiyon yazacaksın.

**Yapman gerekenler:**

1. `read_body(path)` fonksiyonunu yaz: isteği göndersin; `Content-Type`
   başlığı `application/json` ile başlıyorsa `response.json()`, değilse
   `response.text` döndürsün.
2. Üç adresi oku; her biri için adresi, dönen değerin türünün adını
   (`type(...).__name__`) ve değeri yazdır.

**Beklenen çıktı:**

```
/status str ok
/authors/2 dict {'id': 2, 'name': 'Herbert', 'country': 'US', 'born': 1920}
/authors dict 8 authors
```
