`cors_headers(origin)` bir sözlük döndürsün. Her zaman
`"Vary": "Origin"` olsun. `origin` `ALLOWED_ORIGINS` içindeyse ayrıca
`"Access-Control-Allow-Origin": origin` ve
`"Access-Control-Allow-Credentials": "true"`. Başlangıç kodu her kökene
izin veriyor.

**Beklenen çıktı:**

```
https://shop.example
  Access-Control-Allow-Credentials
  Access-Control-Allow-Origin
  Vary
https://notshop.example
  Vary
```
