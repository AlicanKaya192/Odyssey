Stokta bulunan ürünlerin (`stock` sıfırdan büyük) stok adedinin **yarısını**
hesapla.

Sütunlar: `name`, `stock`, `half_stock`. Ada göre sırala.

```
name       stock  half_stock
---------  -----  ----------
Antivirus  99     49.5      
Cable      60     30.0      
...
```

**Dikkat:** `stock` sütunu tam sayı. `stock / 2` yazarsan sonuç da tam sayı
oluyor ve 99'un yarısı **49** çıkıyor — 49,5 değil. Ondalık kısım
yuvarlanmıyor, atılıyor.

Hata almazsın; sadece yanlış sayı görürsün. Sonucun ondalıklı olması için
bölmenin bir tarafını ondalıklı yapman gerekiyor.
