`α`'nın bir adımlık tahmin hatasını nasıl değiştirdiğini ölç, sonra
statsmodels'in bulduğu değerle karşılaştır.

Başlangıç kodunda `adj` hazır: haftalık payı çıkarılmış günlük satış.

**Yapman gerekenler:**

1. `one_step_mae(x, alpha)` fonksiyonunu yaz: düzey
   `x.ewm(alpha=alpha, adjust=False).mean()`; yarının tahmini bugünün düzeyi,
   yani düzeyi `shift(1)` ile kaydır; ilk satırı atıp ortalama mutlak hatayı
   döndür.
2. `α = 0.05, 0.1, 0.2, 0.5, 1.0` için hatayı iki ondalıkla liste olarak
   yazdır.
3. En iyi `α`'nın naife (`α = 1.0`) göre becerisini
   (`1 - MAE / MAE_naive`) iki ondalıkla yazdır.
4. statsmodels ile `α`'yı bul:
   `ExponentialSmoothing(adj).fit().params["smoothing_level"]`; iki ondalığa
   yuvarlayıp yazdır.
5. Aynısını hisse fiyatı (`k`) için yap ve bulunan `α`'yı iki ondalıkla
   yazdır. (İndeksi düzenli olmadığı için `k.to_numpy()` ver.)

**Beklenen çıktı:**

```
[12.55, 11.46, 11.21, 11.83, 13.53]
0.17
0.2
1.0
```

Arındırılmış satışta en iyi `α` küçük: düzey yavaş değişiyor, günlük
oynamanın çoğu gürültü. Hisse fiyatında `α = 1`: düzleştirecek bir şey yok,
en iyi tahmin son değer. Aynı yöntem, iki seri hakkında iki farklı teşhis
koyuyor.
