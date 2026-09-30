`stock_price.csv` bir hissenin günlük kapanış fiyatı. Onu aylığa çevir;
doğru işlemi seçmek sana kalıyor.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `close` sütununu `close` serisine al.
2. Yanlış yolu gör: Mart 2024'ün fiyatlarının **toplamını** iki ondalığa
   yuvarlayıp yazdır.
3. Mart 2024'ün ay sonu kapanışını (`last`) ve aylık ortalamasını (`mean`)
   iki ondalığa yuvarlayıp aynı satıra yazdır.
4. Mart 2024 için `ohlc()` özetinden en yüksek ve en düşük değeri aynı satıra
   yazdır (iki ondalık).
5. Mart 2024 ay sonu kapanışının Şubat 2024 ay sonu kapanışına göre yüzde
   değişimini bir ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
3221.24
166.33 153.39
167.73 140.99
19.3
```

İlk satırdaki sayı hiçbir şeye karşılık gelmiyor: hisse o fiyata hiç satılmadı.
pandas hata vermedi, çünkü neyi ölçtüğünü bilmiyor. Fiyat bir anı gösteriyor;
ayın durumu için son değer, tipik düzeyi için ortalama alınıyor.
