`sales_messy.csv` dosyasında bazı günler eksik. Haftalığa toplarken bu
eksikler toplamı sessizce düşürüyor. Onları yakala.

**Yapman gerekenler:**

1. Dosyayı oku, sırala ve tekrarları topla
   (`sort_index().groupby(level=0).sum()`).
2. Haftalık toplamı ve haftadaki gün sayısını tek tabloda hesapla:
   `resample("W").agg(["sum", "count"])`.
3. 7 günden az gözlemi olan hafta sayısını yazdır.
4. 21 Temmuz 2024'te biten haftanın toplamını ve gün sayısını aynı satıra
   yazdır.
5. O hafta için **ortalamadan** bir tahmin yap: haftanın ortalamasını 7 ile
   çarp, tam sayıya yuvarlayıp yazdır.
6. Seriyi `asfreq("D")` ile takvime oturt, `resample("W").sum(min_count=7)`
   ile topla ve `NaN` çıkan hafta sayısını yazdır.

**Beklenen çıktı:**

```
6
1192 4
2086
6
```

O haftanın gerçek toplamı 1892'ydi. Düz toplam (1192) çok düşük; ortalamadan
yapılan tahmin ise fazla yüksek, çünkü kalan dört gün perşembeden pazara,
yani haftanın yüksek günleri. `min_count` ikisini de yapmıyor: "bu hafta
eksik" diyor.
