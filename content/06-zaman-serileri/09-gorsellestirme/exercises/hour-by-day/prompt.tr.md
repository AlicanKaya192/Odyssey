Saatlik elektrik tüketiminin iki desenini (haftanın günü ve günün saati)
tek bir ısı haritasında göster.

**Yapman gerekenler:**

1. `energy_hourly.csv` dosyasını tarih indeksli oku; `load_mw` sütununu
   `load` serisine al.
2. Gün × saat ortalama tablosunu kur:
   `load.groupby([load.index.dayofweek, load.index.hour]).mean().unstack()`.
3. Tablonun şeklini yazdır.
4. Isı haritasını çiz (`ax.imshow(grid.values, aspect="auto")`), renk
   çubuğunu ekle (`fig.colorbar(image)`) ve `chart.png` olarak kaydet.
5. En yüksek ortalamanın hangi gün (0–6) ve saatte olduğunu ve değerini
   (tam sayı) aynı satıra yazdır. İpucu: `grid.stack().idxmax()` bir
   (gün, saat) çifti veriyor.
6. Aynısını en düşük ortalama için yazdır.
7. Saat 13:00'te pazartesi (0) ve pazar (6) ortalamalarını tam sayıya
   yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
(7, 24)
3 13 1238
6 5 667
1222 1068
```

Tepe hafta içi öğle saatinde, dip pazar sabaha karşı. Aynı saatte pazar,
pazartesinin belirgin biçimde altında: haftanın günü deseni günün her
saatinde geçerli.
