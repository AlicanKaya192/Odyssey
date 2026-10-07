Parquet dosyasındaki siparişleri bellekteki hedef tablosuyla DuckDB'de
birleştir.

**Yapman gerekenler:**

1. `orders.parquet` (300 000 sipariş, `month` sütunuyla) ve pandas tablosu
   `targets` (şehir, hedef) hazır.
2. Tek bir DuckDB sorgusuyla seçilen ayın şehir başına cirosunu
   hesapla, `targets` ile `JOIN ... USING (city)` ile birleştir ve
   yalnızca cirosu hedefe ulaşan şehirleri ciroya göre büyükten küçüğe
   getir.
3. Ay sorguya `?` ile verilsin: `duckdb.execute(sorgu, [MONTH])`.
4. Her satıra şehir, ciro (iki ondalık) ve hedefin yüzde kaçına ulaşıldığını
   (bir ondalık) yazdır.

**Beklenen çıktı:**

```
Ankara 6635981.63 110.6
Izmir 5146542.94 102.9
Antalya 3559928.0 101.7
Trabzon 2047646.76 102.4
```
