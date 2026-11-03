Kayıt satırları `"<zaman> <DURUM> user=<ad> ip=<adres>"` biçiminde,
zaman sırasıyla. `breaches(lines, limit)` en az `limit` başarısız
denemeden **sonra** başarılı (`OK`) giriş gelen adresleri sıralı
döndürsün. Başarısızlığı çok ama başarılı girişi olmayan adres bir alarmdır,
olay değil. Kayıt ve İzleme, Saldırı Tespiti, Olay Müdahalesi.

**Beklenen çıktı:**

```
['10.0.0.7']
[]
```
