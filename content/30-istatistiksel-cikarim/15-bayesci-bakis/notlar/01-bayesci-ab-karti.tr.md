| Kavram | Anlamı | Hesap |
|---|---|---|
| Önsel | veriden önceki inanç | Beta(a, b); düz önsel Beta(1, 1) |
| Sonsal | veriden sonraki inanç | Beta(a + k, b + n − k) |
| İnandırıcı aralık | oran %95 olasılıkla burada | `stats.beta(...).ppf([0.025, 0.975])` |
| P(B > A) | B'nin daha iyi olma olasılığı | örneklerde `(draw_b > draw_a).mean()` |
| Beklenen kayıp | yanlış seçimin ortalama bedeli | `np.maximum(draw_a - draw_b, 0).mean()` |

## Tek fonksiyonda Bayesçi A/B

```python
import numpy as np


def bayes_ab(k_a, n_a, k_b, n_b, seed=0, draws=200_000):
    rng = np.random.default_rng(seed)
    draw_a = rng.beta(1 + k_a, 1 + n_a - k_a, draws)
    draw_b = rng.beta(1 + k_b, 1 + n_b - k_b, draws)
    prob_b = (draw_b > draw_a).mean()
    loss_b = np.maximum(draw_a - draw_b, 0).mean()
    return round(float(prob_b), 3), round(float(loss_b), 5)


print(bayes_ab(472, 4000, 560, 4000))
print(bayes_ab(3, 60, 7, 60))
```

```text
(0.998, 0.0)
(0.896, 0.0026)
```

- Büyük testte P(B > A) bire yakın, B'yi seçmenin beklenen kaybı neredeyse
  sıfır.
- Küçük testte de B önde görünüyor, ama yanılırsak kaybımız çok daha büyük.

## Dikkat

- Önsel veriden **önce** ve gerekçesiyle yazılır.
- Örnek sayısı (`draws`) arttıkça sonuçlar kararlı hâle gelir; tohum
  sabitlenirse her çalıştırmada aynı.
- Karar kuralı (ör. "beklenen kayıp 0,001'in altına inince seç") testten
  önce yazılır.
