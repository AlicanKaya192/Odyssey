Her olay `[zaman, kaynak, metin]`; zamanlar farklı saat dilimlerinde
(`Z`, `+00:00`, `+03:00`...). `utc_timeline(events)` olayları **UTC**'ye
çevirip zamana göre sıralasın ve `"HH:MM:SS kaynak metin"` satırları
döndürsün (saat UTC). Metin olarak sıralamak yanıltır. Kayıt ve İzleme,
Adli Bilişim.

**Beklenen çıktı:**

```
09:00:05 auth reset
09:00:05 fw block
09:00:10 web login
09:00:20 db query
```
