`passengers_monthly.csv` aylık yolcu sayısı (bin), 2013–2024. Seri büyüyor
ve mevsimsel dalgaları da onunla birlikte büyüyor. Aynı seriyi iki eksenle
yan yana çiz.

**Yapman gerekenler:**

1. Dosyayı `index_col="month"` ve `parse_dates=True` ile oku; `passengers`
   sütununu `p` serisine al.
2. Yıl bazında en düşük ve en yüksek ayı bul
   (`p.groupby(p.index.year).agg(["min", "max"])`).
3. 2013 ve 2024 için yaz–kış **farkını** (`max - min`) aynı satıra yazdır.
4. Aynı iki yıl için yaz–kış **oranını** (`max / min`) iki ondalığa
   yuvarlayıp aynı satıra yazdır.
5. Yan yana iki panel aç (`plt.subplots(1, 2, figsize=(11, 4))`), ikisine de
   seriyi çiz; ikincisinin dikey eksenini logaritmik yap
   (`set_yscale("log")`) ve `chart.png` olarak kaydet.
6. İki panelin dikey eksen ölçeğini liste olarak yazdır
   (`ax.get_yscale()`).

**Beklenen çıktı:**

```
61 183
1.6 1.6
['linear', 'log']
```

Fark üç katına çıkmış, oran hiç değişmemiş: mevsimsellik serinin düzeyiyle
orantılı. Doğrusal panelde dalgalar yıllar geçtikçe büyüyor; logaritmik
panelde hepsi aynı boyda ve çizgi neredeyse düz.
