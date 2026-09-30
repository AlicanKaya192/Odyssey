2024'ün her günü için "yarını" beş temel yöntemle tahmin et ve puan
tablosunu çıkar. Her tahmin yalnızca **o günden önceki** veriyi kullanmalı.

**Yapman gerekenler:**

1. Beş tek adımlı tahmini bütün seri üzerinde kur (bir sözlükte, bu sırayla):
   - `"mean so far"`: o güne kadarki bütün geçmişin ortalaması
     (`s.shift(1).expanding().mean()`)
   - `"mean of 7"`: son 7 günün ortalaması
   - `"naive"`: dünkü değer
   - `"seasonal naive"`: geçen haftanın aynı günü
   - `"mean of 4 weeks"`: son dört haftanın aynı günlerinin ortalaması
     (`s.shift(7)`, `s.shift(14)`, `s.shift(21)`, `s.shift(28)`)
2. Her biri için 2024'teki ortalama mutlak hatayı ve yanlılığı `ad MAE
   yanlılık` biçiminde, iki ondalıkla, alt alta yazdır.
3. En iyi yöntemin naife göre becerisini (`1 - MAE / MAE_naive`) iki ondalığa
   yuvarlayıp yazdır.
4. **Sızıntı deneyi:** "son dört haftanın ortalaması"nı yanlış kurup bugünü de
   içine alsaydın (`(s + s.shift(7) + s.shift(14) + s.shift(21)) / 4`) MAE ne
   çıkardı? İki ondalıkla yazdır.

**Beklenen çıktı:**

```
mean so far 52.48 43.49
mean of 7 42.74 0.22
naive 41.1 -0.16
seasonal naive 13.87 0.92
mean of 4 weeks 13.89 2.03
0.66
9.86
```

Haftalık deseni kullanan iki yöntem açık ara önde ve birbirine çok yakın.
Yanlılık dördünde sıfıra yakın; yalnızca bütün geçmişin ortalaması sistematik
olarak düşük (seri büyüyor, eski yıllar ortalamayı aşağı çekiyor). Son satır
sızıntının neye benzediğini gösteriyor: tablonun en iyi sonucu, ama sahte.
Tahmin kendi hedefini ortalamanın içinde görüyor; gerçekte o günü bilmeden bu
tahmini yapamazdın. **Fazla iyi bir sonuç gördüğünde önce sızıntı ara.**
