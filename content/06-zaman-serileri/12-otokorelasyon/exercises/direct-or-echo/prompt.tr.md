`temperature_daily.csv` altı yıllık günlük sıcaklık (`date`, `temp_c`).
Mevsim normalinden sapmanın hafızası ne kadar uzun ve ne kadarı doğrudan?

**Yapman gerekenler:**

1. Mevsim normalini hesapla: her takvim günü için altı yılın ortalaması
   (`t.groupby(t.index.dayofyear).transform("mean")`). Sapma: `anomaly = t -
   normal`.
2. Sapmanın ACF'sini ilk 5 gecikme için iki ondalığa yuvarlayıp liste olarak
   yazdır (gecikme 0 hariç).
3. Sapmanın PACF'sini aynı 5 gecikme için yazdır.
4. "Yalnızca dün etkili" olsaydı ACF `r, r², r³, ...` diye sönerdi. `r`'yi 1.
   gecikmenin ACF'si alıp ilk 5 kuvvetini iki ondalığa yuvarlayarak liste
   olarak yazdır.
5. Ham sıcaklığın (`t`) 1. ve 365. gecikmedeki ACF'sini iki ondalığa
   yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
[0.72, 0.51, 0.38, 0.28, 0.19]
[0.72, -0.03, 0.06, -0.02, -0.03]
[0.72, 0.52, 0.38, 0.27, 0.2]
0.97 0.74
```

ACF uzun bir kuyruk gösteriyor ama PACF'de yalnızca 1. gecikme var: iki gün
öncesi bugünü doğrudan etkilemiyor. Üçüncü satır bunu doğruluyor: `r`'nin
kuvvetleri gerçek ACF'ye çok yakın. Ham sıcaklıkta ise 365. gecikme hâlâ çok
yüksek: bu hafıza değil, yıllık mevsim.
