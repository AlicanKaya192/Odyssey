Mevsimsel naifi 2024 boyunca 13 farklı başlangıçtan sına ve sonuçları
çubuk grafiğiyle kaydet. Başlangıç kodunda `snaive(train, h)` hazır.

**Yapman gerekenler:**

1. 13 deney yap. `i`. deneyin kesim günü
   `pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i)`. Eğitim kesime
   kadar (`s.loc[:cut]`), test sonraki 28 gün
   (`s.loc[cut + pd.Timedelta(days=1):].iloc[:28]`).
2. Her deneyde MAE'yi ve yanlılığı hesapla; kesim günüyle birlikte sakla.
3. Deney sayısını, MAE'lerin ortalamasını, standart sapmasını (`ddof=1`), en
   küçüğünü ve en büyüğünü iki ondalıkla aynı satıra yazdır.
4. En kötü iki deneyin kesim günlerini `"%Y-%m-%d"` listesi olarak yazdır
   (tarih sırasıyla).
5. 5 Kasım 2024 kesimli deneyin MAE'sini ve bütün deneylerin ortalama
   yanlılığını iki ondalıkla aynı satıra yazdır.
6. 13 MAE'nin çubuk grafiğini çiz ve `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
13 17.95 10.94 9.39 41.29
['2024-01-02', '2024-12-03']
11.64 1.68
```

Tipik hata 18 dolayında, ama döneme göre 9 ile 41 arasında oynuyor. En kötü
iki deney yılın başı ve sonu. Bölüm 14'te ölçtüğün 11.64 bu 13 deneyden
yalnızca biri ve iyi olanlardan. Tek bir sayı yerine artık bir dağılımın
var.
