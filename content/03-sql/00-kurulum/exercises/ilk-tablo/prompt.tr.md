Sunucuda **`sehirler`** adında bir tablo hazır duruyor. İçinde beş şehir
var; her satırda şehrin adı, ülkesi ve nüfusu yazıyor.

Görevin bu tablonun **tamamını** ekrana getirmek.

İki kelimeyle oluyor:

- `SELECT` — "şunu getir" demek. Yanına `*` yazarsan "bütün sütunlar"
  anlamına geliyor.
- `FROM` — "şu tablodan" demek.

Sonuç beş satır, dört sütun olmalı:

```
id  ad         ulke      nufus
--  ---------  --------  --------
1   Istanbul   Turkiye   15840900
...
```

Satırların sırası önemli değil; sunucu hangi sırayla verirse o kabul.
