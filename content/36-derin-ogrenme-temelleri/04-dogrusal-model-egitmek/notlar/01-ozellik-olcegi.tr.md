Öğrenme oranı tek başına seçilmez; girdinin ölçeğine bağlıdır. Aynı
noktaları santim yerine milimetreyle ölçtüğümüzü düşünelim (`x · 100`):

```python
import math


def fit(inputs, lr, steps=100):
    w = torch.zeros(1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    for _ in range(steps):
        loss = ((w * inputs + b - y) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()
    return loss.item()


big = x * 100
print(math.isfinite(fit(big, 0.05)), round(fit(big, 0.00001), 2))
scaled = (big - big.mean()) / big.std()
print(round(fit(scaled, 0.05), 3))
```

```text
False 1.23
0.235
```

- Girdi 100 kat büyüyünce `w`'nin gradyanı da büyüyor; dersteki uygun
  `lr = 0.05` artık ıraksıyor: sonuç sonlu bir sayı bile değil (`math.isfinite`
  `False`), kayıp taşıp `nan` olmuş.
- Öğrenme oranını küçültmek patlamayı durduruyor ama bu kez `b` çok yavaş
  öğreniyor; 100 turda kayıp hâlâ yüksek (1,23).
- Girdiyi **ölçeklemek** (ortalaması 0, standart sapması 1) ikisini de
  çözüyor: aynı `lr = 0.05` ile kayıp yine gürültü düzeyine iniyor.

Bu yüzden derin öğrenmede girdiler hemen her zaman ölçeklenir: piksel
değerlerini 0–1'e çekmek, tablo sütunlarını standartlaştırmak. Giriş
bölümündeki `/ 16` da bunun için.
