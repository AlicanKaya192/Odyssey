`orders_raw.csv` temizlenmemiş hâli: bazı `ordered_at` değerleri tarih
bile değil. `errors="coerce"` ile oku, ama körlemesine değil.

**Yapman gerekenler:**

1. Dosyayı oku. `ordered_at` sütununu `format="%d.%m.%Y %H:%M"` ve
   `errors="coerce"` ile çevirip `ordered` adlı yeni bir sütuna yaz.
2. Kaç değerin `NaT` olduğunu yazdır.
3. `NaT` olan satırların **ham** `ordered_at` değerlerini liste olarak
   yazdır.
4. Bozuk satırları at (`dropna(subset=["ordered"])`) ve kalan satır sayısını
   yazdır.
5. Kalan tablodaki en erken sipariş zamanını yazdır.

**Beklenen çıktı:**

```
3
['31.02.2024 10:15', 'unknown', '00.00.0000 00:00']
237
2024-01-03 05:12:00
```

Üç bozuk değer üç farklı türde: takvimde olmayan bir gün (31 Şubat), tarih
olmayan bir kelime ve sıfırlarla doldurulmuş bir yer tutucu. Hangilerinin
bozuk olduğunu görmeden atsaydın, biçimi yanlış yazdığın bir gün verinin
yarısını fark etmeden silerdin.
