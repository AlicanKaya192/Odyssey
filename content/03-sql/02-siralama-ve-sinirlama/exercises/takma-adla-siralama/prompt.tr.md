Bu alıştırma bölümün üç parçasını bir araya getiriyor.

**Stokta bulunan** ürünleri getir (`stock` sıfırdan büyük), `name` sütunu
`product`, `price` sütunu `amount` başlığıyla gelsin ve sonuç **`amount`
değerine göre büyükten küçüğe** sıralansın.

```
product  amount 
-------  -------
Laptop   24500.0
Desktop  18900.0
...
```

Sonuç altı satır olmalı.

Buradaki asıl nokta şu: **`ORDER BY` takma adı kullanabiliyor.** Geçen
bölümde aynı takma adı `WHERE` içinde kullanmayı denesen hata alırdın —
`WHERE` erken, `ORDER BY` geç çalışıyor.
