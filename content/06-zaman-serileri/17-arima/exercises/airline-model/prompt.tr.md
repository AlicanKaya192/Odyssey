Aylık yolcu serisine mevsimsel ARIMA kur: logaritma, bir fark, bir
mevsimsel fark, birer MA terimi. 2024'ü tahmin et ve grafiğini kaydet.

Başlangıç kodunda `train` (2023 sonuna kadar) ve `test` (2024) hazır.

**Yapman gerekenler:**

1. Modeli logaritma üzerinde kur:
   `ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()`.
2. İki MA katsayısını (`ma.L1`, `ma.S.L12`) iki ondalıkla aynı satıra yazdır.
3. 12 aylık tahmini al ve `np.exp` ile geri çevir. Ortalama mutlak hatayı
   (iki ondalık) ve yüzde hatayı (bir ondalık) aynı satıra yazdır.
4. Aynı modeli logaritma **almadan** kur ve ortalama mutlak hatasını iki
   ondalıkla yazdır.
5. Kalıntı denetimi: logaritmalı modelin kalıntısının ilk 13 değerini at
   (`fit.resid.iloc[13:]`) ve 12 gecikmeli Ljung–Box p-değerini iki ondalıkla
   yazdır.
6. Ağustos 2024 için tahmini ve gerçek değeri tam sayıya yuvarlayıp aynı
   satıra yazdır.
7. Grafik çiz: 2022–2024 gerçek değerler ve 2024 tahmini. `chart.png` olarak
   kaydet.

**Beklenen çıktı:**

```
-0.94 -0.95
6.14 1.6
11.05
0.99
493 480
```

İki katsayılı model on iki ayı ortalama %1.6 hatayla tahmin ediyor ve
kalıntısında hafıza kalmamış (p-değeri büyük). Logaritma atlanınca hata
neredeyse iki katına çıkıyor: dönüşüm modelin parçası. Bölüm 14'ün çıtası
11.11, Holt–Winters 6.53 idi.
