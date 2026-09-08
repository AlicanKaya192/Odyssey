Bu alıştırma bölümün üç parçasını bir araya getiriyor.

**Stokta bulunan** ürünleri getir (`stok` sıfırdan büyük), `ad` sütunu
`urun`, `fiyat` sütunu `tutar` başlığıyla gelsin ve sonuç **`tutar`
değerine göre büyükten küçüğe** sıralansın.

```
urun      tutar
--------  ---------
Laptop    24500.00
Masaustu  18900.00
...
```

Sonuç altı satır olmalı.

Buradaki asıl nokta şu: **`ORDER BY` takma adı kullanabiliyor.** Geçen
bölümde aynı takma adı `WHERE` içinde kullanmayı denesen hata alırdın —
`WHERE` erken, `ORDER BY` geç çalışıyor.
