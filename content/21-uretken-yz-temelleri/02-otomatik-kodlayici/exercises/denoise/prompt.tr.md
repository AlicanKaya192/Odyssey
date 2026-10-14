`denoise(k, sigma, seed)` test resimlerine `np.random.default_rng(seed).normal(0,
sigma, X_test.shape)` gürültüsü eklesin, gürültülü resimleri eğitim verisinin
ilk `k` PCA yönüyle kodlayıp geri kursun ve iki hatayı döndürsün:
`[gürültülü ile temiz arası, geri kurulan ile temiz arası]`, 4 basamağa
yuvarlanmış `float`.

**Beklenen çıktı:**

```
8 [0.0396, 0.0296]
16 [0.0396, 0.0213]
32 [0.0396, 0.0222]
```
