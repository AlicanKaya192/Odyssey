Günlük satışın korelogramını mevsimsel farktan önce ve sonra karşılaştır,
farktan sonraki korelogramı çizip kaydet.

**Yapman gerekenler:**

1. `d7 = s.diff(7).dropna()` hesapla.
2. Serinin ve `d7`'nin ACF'sini 21 gecikmeyle hesapla. Her birinde gecikme 0
   hariç, mutlak değeri `1.96 / np.sqrt(len(x))` bandını aşan gecikme sayısını
   aynı satıra yazdır (önce seri).
3. `d7`'nin ACF'sini 1, 7 ve 14. gecikmelerde iki ondalığa yuvarlayıp liste
   olarak yazdır.
4. `d7`'de mutlak değeri en büyük gecikmeyi ve değerini (iki ondalık) aynı
   satıra yazdır.
5. `d7`'nin korelogramını çiz ve kaydet: `fig = plot_acf(d7, lags=21)`, sonra
   `fig.savefig("chart.png")`.

**Beklenen çıktı:**

```
21 6
[0.16, -0.41, 0.02]
7 -0.41
```

Ham seride neredeyse her gecikme bandın dışında: mevsim ve trend her şeyi
dolduruyor. Farktan sonra geriye asıl yapı kalıyor: 1. gecikmede küçük bir artı
ve 7. gecikmede belirgin bir eksi. 14. gecikmede bir şey yok: geçen haftanın
sürprizi bu haftayı etkiliyor, iki hafta öncesi etkilemiyor. Sol taraftaki
**Çıktı** sekmesinde 7. gecikmedeki çubuğu gör.
