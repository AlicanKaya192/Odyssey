Üç yıllık günlük satışı çiz ve `chart.png` olarak kaydet.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını tarih indeksli `s` serisi olarak oku.
2. `figsize=(10, 4)` ile bir tuval aç ve seriyi ince bir çizgiyle çiz:
   `ax.plot(s.index, s.values, linewidth=0.8)`.
3. Başlığı `Daily sales`, dikey eksen etiketini `Units` yap.
4. Grafiği `chart.png` olarak kaydet.
5. Çizgi sayısını (`len(ax.lines)`), başlığı ve dikey eksen etiketini alt
   alta yazdır.
6. Tuvalin genişliğini ve yüksekliğini aynı satıra yazdır
   (`fig.get_size_inches()`).

**Beklenen çıktı:**

```
1
Daily sales
Units
10.0 4.0
```

Grafik sol taraftaki **Çıktı** sekmesinde görünecek. Yükselen trendi, her yıl
sonundaki tepeyi ve haftalık zikzağın oluşturduğu kalın bandı ara.
