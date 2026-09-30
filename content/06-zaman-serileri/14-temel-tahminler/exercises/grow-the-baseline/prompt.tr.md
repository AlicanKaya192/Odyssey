Yolcu serisinde 2024'ü üç yolla tahmin et: düz mevsimsel naif, üstüne
kayma ekleyerek ve büyüme oranıyla çarparak.

Başlangıç kodunda `train` (2023 sonuna kadar) ve `test` (2024) hazır.

**Yapman gerekenler:**

1. `base`: 2023'ün on iki değeri (`train.loc["2023"].to_numpy()`).
2. **Kayma:** eğim `(train.iloc[-1] - train.iloc[0]) / (len(train) - 1)`.
   Bir yıl sonrası için her aya `slope * 12` ekle.
3. **Büyüme:** oran `train.loc["2023"].sum() / train.loc["2022"].sum()`.
   Her ayı bu oranla çarp. Oranı dört ondalığa yuvarlayıp yazdır.
4. Üç tahmin için ortalama mutlak hatayı ve yüzde hatayı
   (`(|hata| / gerçek)` ortalaması × 100) `ad MAE yüzde` biçiminde alt alta
   yazdır (MAE iki, yüzde bir ondalık; sıra: snaive, drift, growth).
5. Büyümeli tahminin düz mevsimsel naife göre becerisini
   (`1 - MAE_growth / MAE_snaive`) iki ondalığa yuvarlayıp yazdır.
6. Ağustos 2024 için gerçek değeri ve üç tahmini tam sayıya yuvarlayıp aynı
   satıra yazdır.

**Beklenen çıktı:**

```
1.0993
snaive 40.42 10.3
drift 18.52 4.6
growth 11.11 2.8
0.73
480 448 470 492
```

Düz kopya %10 yanılıyor, kayma eklenince %5'in altına, büyüme oranıyla
çarpınca %3'ün altına iniyor. Büyüme oranını yalnızca eğitim verisinden
(2023 / 2022) hesapladın; 2024'ü kullansaydın sızıntı olurdu. Bundan sonra bu
serinin çıtası düz mevsimsel naif değil, büyümeli hâli.
