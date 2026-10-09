`gradient_boost_1d(x, y, rounds, lr)` fonksiyonunu yaz: tahmin ortalamayla
başlar; `rounds` kez artıklara hazır `fit_stump_reg` ile kütük uydur ve
tahmine `lr ×` kütüğün çıktısını ekle (`x ≤ eşik` ise sol ortalama, değilse
sağ). Son eğitim MSE'sini `round(..., 4)` ile döndürsün.

**Beklenen çıktı:**

```
0 7.3325
1 3.13
5 0.0814
30 0.0048
```
