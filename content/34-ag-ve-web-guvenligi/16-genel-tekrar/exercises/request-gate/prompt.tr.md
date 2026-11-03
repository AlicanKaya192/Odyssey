CSRF ve Güvenli API bölümlerini birleştir. `gate(req, sessions, notes)`
bir durum kodu döndürsün:

- çerezin oturumu yoksa `401`,
- `POST`'ta `origin` `ALLOWED_ORIGINS`'te değilse ya da `csrf`
  oturumunkiyle tutmuyorsa (`compare_digest`) `403`,
- not yoksa ya da sahibi oturumun kullanıcısı değilse `404`,
- yoksa `200`.

**Beklenen çıktı:**

```
200
404
401
403
200
```
