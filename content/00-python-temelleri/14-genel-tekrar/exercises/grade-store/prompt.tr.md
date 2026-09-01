Son alıştırma: veritabanı, hata yakalama ve tip belirtimleri bir arada.

Bağlantı ve tablo senin için hazır.

**Yapman gerekenler:**

1. `save(name, raw)` fonksiyonu — belirtimi `(str, str) -> bool`:
   - `raw` metnini sayıya çevirmeyi dene.
   - Çevrilirse satırı ekle, `commit` çağır ve `True` döndür.
   - Çevrilemezse (`ValueError`) **hiçbir şey ekleme** ve `False` döndür.

2. `find(name)` fonksiyonu — belirtimi `(str) -> int | None`:
   - O ismin notunu döndürsün, isim yoksa `None` döndürsün.

3. `average()` fonksiyonu — belirtimi `() -> int`:
   - Tablodaki notların ortalamasını **tam sayıya yuvarlanmış** döndürsün.
   - Tablo boşsa `0` döndürsün. (`AVG` boş tabloda `None` veriyor.)

4. Şu değerleri sırayla kaydet ve her sonucu yazdır:
   `("Ada", "90")`, `("Brian", "oops")`, `("Grace", "76")`

5. Sonra sırayla şunları yazdır: `find("Ada")`, `find("Nobody")`, `average()`

**Beklenen çıktı:**

```
True
False
True
90
None
83
```

Ortalama: `(90 + 76) / 2 = 83.0`. Brian hiç kaydedilmedi.

> `AVG` boş tabloda `None` döndürüyor; `average` içinde bunu kontrol etmen
> gerekiyor.
