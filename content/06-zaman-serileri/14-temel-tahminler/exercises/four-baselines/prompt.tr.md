Dört temel tahmini kur, ölç ve grafiğini kaydet.

Başlangıç kodunda `train`, `test`, `h` ve `future` hazır.

**Yapman gerekenler:**

1. Dört tahmini, indeksi `future` olan birer seri olarak kur:
   - `mean_fc`: eğitim ortalaması
   - `naive_fc`: eğitimin son değeri
   - `snaive_fc`: son haftanın tekrarı (`last_week[i % 7]`)
   - `drift_fc`: son değer + eğim × adım; eğim
     `(train.iloc[-1] - train.iloc[0]) / (len(train) - 1)`, adımlar
     `np.arange(1, h + 1)`
2. Her birinin ortalama mutlak hatasını `ad hata` biçiminde, iki ondalıkla,
   alt alta yazdır (sıra: mean, naive, snaive, drift).
3. İlk test günü (6 Kasım) için gerçek değeri ve dört tahmini tam sayıya
   yuvarlayıp aynı satıra yazdır.
4. Grafik çiz: eğitimin son 28 günü ve test (gri), üstüne dört tahmin.
   `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
mean 75.98
naive 64.07
snaive 11.64
drift 64.6
283 255 267 286 267
```

Mevsimsel naif öbür üçünden beş altı kat isabetli. Sol taraftaki **Çıktı**
sekmesinde nedenini göreceksin: ortalama, naif ve kayma düz birer çizgi;
yalnızca mevsimsel naif haftalık deseni izliyor.
