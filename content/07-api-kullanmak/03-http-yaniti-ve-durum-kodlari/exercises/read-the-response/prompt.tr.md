Ham bir yanıt metni elinde: `429` ile gelmiş. Bir istek kütüphanesinin
yanıtı okurken yaptığını sen yapacaksın.

**Yapman gerekenler:**

1. `parse_response(raw)` fonksiyonunu yaz. Metni ilk boş satırdan
   (`"\n\n"`) ikiye ayırsın; ilk satırdan kodu (int), sonraki satırlardan
   başlıkları (adlar küçük harfle) alsın. Şunu döndürsün:
   `{"code": ..., "headers": {...}, "body": ...}`.
2. `response = parse_response(raw)` ile yanıtı oku ve şunları yazdır:
   - kod,
   - içerik türünün **noktalı virgülden önceki** kısmı,
   - `Retry-After` değeri **sayı** olarak, `wait 30 seconds` biçiminde,
   - gövde.

**Beklenen çıktı:**

```
429
application/json
wait 30 seconds
{"error": "rate limit", "limit": 60}
```
