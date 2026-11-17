`one_step(w_value, b_value, xs, ys, lr)` doğrusal model için **tek** bir gradyan
inişi adımı atsın: MSE kaybını hesapla, `backward()`, iki parametreyi
`torch.no_grad()` içinde güncelle. Yeni `[w, b]`'yi 4 basamakla döndür.

**Beklenen çıktı:**

```
[1.3, 0.8]
[1.0, 1.0]
```
