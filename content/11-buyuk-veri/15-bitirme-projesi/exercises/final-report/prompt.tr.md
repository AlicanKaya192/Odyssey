Parquet dosyasından yöneticiye kısa bir rapor çıkar: kesin sayılar
DuckDB'den, hızlı tahmin örneklemden.

**Yapman gerekenler:**

1. `orders.parquet` hazır (300 000 sipariş, `month` sütunuyla).
2. DuckDB: ciroda ilk üç şehri ve her birinin toplam ciro içindeki payını
   (yüzde, bir ondalık) bul; her satıra şehir ve pay.
3. DuckDB: sipariş başına ortalama cironun en yüksek olduğu ayı ve o
   ortalamayı (iki ondalık) yazdır.
4. Hızlı tahmin: dosyayı pandas ile oku, `sample(frac=0.01,
   random_state=3)` ile örneklem al; sipariş başına ortalama ciroyu
   örneklemden ve tamamından hesapla. İkisini (iki ondalık) ve hatayı
   (yüzde, bir ondalık) aynı satıra yazdır.

**Beklenen çıktı:**

```
Istanbul 34.0
Ankara 15.9
Izmir 13.2
2024-05 1665.57
1627.57 1642.77 0.9
```
