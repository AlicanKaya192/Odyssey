| Metrik türü | Etki büyüklüğü | Formül |
|---|---|---|
| Ortalama | Cohen's d | $(\bar{x}_B - \bar{x}_A) / s_p$ |
| Oran | Risk farkı | $p_B - p_A$ |
| Oran | Göreli risk | $p_B / p_A$ |
| Oran | Odds oranı | $\frac{p_B / (1 - p_B)}{p_A / (1 - p_A)}$ |
| Oran | Cohen's h | $2\arcsin\sqrt{p_B} - 2\arcsin\sqrt{p_A}$ |
| İki grup, sıralı | Ortak dil | $U / (n_A n_B)$ |
| Çok grup | η² (eta kare) | grup arası kareler / toplam kareler |
| Çapraz tablo | Cramér's V | `stats.contingency.association` |

Kaba ölçüt (d ve h): 0,2 küçük, 0,5 orta, 0,8 büyük. Alan bilgisi her
zaman önce gelir.

## Hepsi bir arada

```python
import numpy as np


def rate_effects(p_a, p_b):
    odds_a, odds_b = p_a / (1 - p_a), p_b / (1 - p_b)
    h = 2 * np.arcsin(np.sqrt(p_b)) - 2 * np.arcsin(np.sqrt(p_a))
    return [round(p_b - p_a, 3), round(p_b / p_a, 2),
            round(odds_b / odds_a, 2), round(float(h), 3)]


print(rate_effects(0.10, 0.12))
print(rate_effects(0.50, 0.60))
```

```text
[0.02, 1.2, 1.23, 0.064]
[0.1, 1.2, 1.5, 0.201]
```

- İki satırda da göreli risk benzer, ama risk farkı ve h çok farklı.
- Taban oranı yükselince odds oranı göreli riskten uzaklaşır.

## Raporlama sırası

1. İki grubun değerleri (ortalamalar ya da oranlar), n'ler.
2. Fark ve güven aralığı, metriğin kendi biriminde.
3. Standart etki büyüklüğü (d, h) gerekiyorsa.
4. p değeri.
5. Önceden belirlenmiş pratik eşikle karşılaştırma.
