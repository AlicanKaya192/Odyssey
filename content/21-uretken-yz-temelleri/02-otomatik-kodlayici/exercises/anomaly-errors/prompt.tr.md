`anomaly_errors(k)` PCA'yı **yalnızca 0–4 rakamlarının** eğitim resimleriyle
kursun (`y_train = y[order[:1500]]`). Sonra her test resmini ilk `k` yönle
geri kurup resim başına ortalama kare hatayı bulsun ve iki ortalama
döndürsün: `[0–4 test resimlerinin ortalama hatası, 5–9 test resimlerinin
ortalama hatası]`, 4 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[0.0199, 0.0398]
[0.009, 0.0214]
```
