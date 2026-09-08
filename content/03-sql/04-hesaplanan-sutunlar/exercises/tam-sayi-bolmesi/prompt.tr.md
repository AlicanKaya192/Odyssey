Stokta bulunan ürünlerin (`stok` sıfırdan büyük) stok adedinin **yarısını**
hesapla.

Sütunlar: `ad`, `stok`, `yari_stok`. Ada göre sırala.

```
ad         stok  yari_stok
---------  ----  ---------
Antivirus  99    49.500000
Kablo      60    30.000000
...
```

**Dikkat:** `stok` sütunu tam sayı. `stok / 2` yazarsan sonuç da tam sayı
oluyor ve 99'un yarısı **49** çıkıyor — 49,5 değil. Ondalık kısım
yuvarlanmıyor, atılıyor.

Hata almazsın; sadece yanlış sayı görürsün. Sonucun ondalıklı olması için
bölmenin bir tarafını ondalıklı yapman gerekiyor.
