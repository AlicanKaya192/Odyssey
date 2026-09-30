Üç yılı üst üste koyan mevsim grafiğini çiz: yatay eksende ay, her yıl
bir çizgi.

**Yapman gerekenler:**

1. Dosyayı oku. Ay ve yıla göre ortalama tablosunu kur:
   `s.groupby([s.index.month, s.index.year]).mean().unstack()`.
2. Tablonun şeklini (`shape`) ve sütunlarını liste olarak yazdır.
3. Her yıl için bir çizgi çiz (`marker="o"`, etiket yılın kendisi), lejant
   ekle ve `chart.png` olarak kaydet.
4. Her yılın en düşük ve en yüksek ayını `yıl düşük yüksek` biçiminde alt
   alta yazdır (`idxmin()`, `idxmax()`).
5. Her ayda 2024'ün 2022'den ne kadar yüksek olduğunu hesapla ve bu farkların
   ortalamasını bir ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
(12, 3)
[2022, 2023, 2024]
2022 5 12
2023 6 12
2024 5 12
68.5
```

Üç yılda da tepe Aralık, dip Mayıs ya da Haziran: çizgilerin şekli aynı, yani
mevsimsellik kararlı. Aralarındaki mesafe ise trend: 2024, 2022'nin her ay ortalama 68
birim üstünde.
