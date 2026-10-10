Üç günün üç ürün fiyatı bir matriste: satır gün, sütun ürün. Yayınlamayla her
hesap tek satır:

```python
import numpy as np

prices = np.array([[100, 50, 20], [110, 45, 22], [121, 54, 21]], dtype=float)
change = (prices[1:] / prices[:-1] - 1) * 100
print(change.round(1).tolist())
low, high = prices.min(axis=0), prices.max(axis=0)
print(((prices - low) / (high - low)).round(2).tolist())
weights = np.array([0.5, 0.3, 0.2])
print((prices * weights).sum(axis=1).tolist(), (prices @ weights).tolist())
share = prices / prices.sum(axis=1, keepdims=True)
print(share.sum(axis=1).round(10).tolist())
```

```text
[[10.0, -10.0, 10.0], [10.0, 20.0, -4.5]]
[[0.0, 0.56, 0.0], [0.48, 0.0, 1.0], [1.0, 1.0, 0.5]]
[69.0, 72.9, 80.9] [69.0, 72.9, 80.9]
[1.0, 1.0, 1.0]
```

## Satır satır

| Hesap | Nasıl yayıldı |
|---|---|
| Günlük yüzde değişim | `prices[1:]` / `prices[:-1]`: aynı şekil, bir gün kaydırılmış |
| Min-max ölçekleme (0–1) | `(3, 3)` − `(3,)`: her sütunun en küçüğü her satırdan |
| Ağırlıklı sepet değeri | `(3, 3)` × `(3,)` sonra satır toplamı; ya da matris çarpımı `@` |
| Günün içindeki pay | satır toplamı `keepdims=True` ile `(3, 1)`; her satırın payları 1'e toplanır |

## İki yol aynı sonuç

`(prices * weights).sum(axis=1)` ile `prices @ weights` aynı sayıları verdi.
İlki yayınlama + toplama, ikincisi matris-vektör çarpımı. Büyük matrislerde
`@` daha hızlıdır (doğrusal cebir kütüphanesine gider) ve niyeti daha açık
söyler: "her satırın ağırlıklarla iç çarpımı". Matris çarpımı bir sonraki
bölümün (linalg) konusu.

## Dikkat

- Yüzde değişimde ilk günün değişimi yok: sonuç 2 satır.
- Min-max ölçeklemede bir sütun sabitse (`high == low`) sıfıra bölünür;
  `np.where(high > low, ..., 0)` ile korunur.
