Aynı veriyi aya ve güne göre böl; dosya sayısını ve toplam boyutu
karşılaştır.

**Yapman gerekenler:**

1. `make_orders(50_000)` ile tabloyu kur, `order_time`'ı tarihe çevir.
   `month` (`%Y-%m`) ve `day` (`%Y-%m-%d`) sütunlarını ekle.
2. Aya göre `by_month/month=.../part-0.parquet`, güne göre
   `by_day/day=.../part-0.parquet` olarak yaz. Her dosyadan `month` ve
   `day` sütunlarının ikisini de çıkar.
3. İki klasör için bir satıra klasörün adını, dosya sayısını ve toplam
   boyutunu kilobayt olarak (bir ondalık) yazdır
   (`rglob("*.parquet")`, `stat().st_size`).
4. Son satıra gün düzeninin toplamının ay düzeninin toplamına oranını (iki
   ondalık) yazdır.

**Beklenen çıktı:**

```
by_month 12 1366.6
by_day 366 3164.8
2.32
```

Aynı veri, aynı satırlar; ama günlük düzende her dosya kendi altbilgisini ve
sözlüğünü taşıdığı için toplam büyüyor.
