Siparişler kaç günde teslim ediliyor? `orders_raw.csv` dosyasında iki
sütun da sorunlu: `ordered_at` gün önde ve saatli, `delivered_on` ISO ama bazı
satırlarda boş ya da `not delivered`.

**Yapman gerekenler:**

1. `ordered_at` sütununu `format="%d.%m.%Y %H:%M"` ve `errors="coerce"` ile
   çevir.
2. `delivered_on` sütununu `errors="coerce"` ile çevir.
3. Teslim süresini gün olarak hesapla:
   `(delivered - ordered.dt.normalize()).dt.days`.
4. Sırayla yazdır: süresi hesaplanabilen sipariş sayısı, ortalama süre (iki
   ondalık), en uzun süre (tam sayı), 3 günden uzun süren sipariş sayısı.

**Beklenen çıktı:**

```
230
2.33
8
33
```

240 siparişin 10'unda taraflardan biri `NaT`; pandas onları ortalamaya
katmadı. `normalize()` olmasaydı sipariş saati farktan düşülür ve akşam
verilen siparişler bir gün kısa görünürdü.
